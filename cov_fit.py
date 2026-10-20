#-----------------------------------------------------------------------#
# cov_fit.py v1.0.0
# By Hunter Brooks, at UToledo, Toledo
#-----------------------------------------------------------------------#


# Import Packages
#-----------------------------------------------------------------------#
import argparse
import numpy as np
import pandas as pd
#-----------------------------------------------------------------------#


# Function to predict dependent variable (y) and its uncertainty
#-----------------------------------------------------------------------#
def predict_dependent_value(x_val, x_err_val, summary_csv_path, cov_csv_path):
    
    # 1. Load CSV files
    summary_df = pd.read_csv(summary_csv_path)
    cov_df = pd.read_csv(cov_csv_path, index_col=0)

    # Extract coefficients and metadata from summary
    a_rows = summary_df[summary_df["param"].str.startswith("a")]
    a_coeffs = a_rows["mean"].values
    order = int(summary_df["order"].iloc[0])

    # Get intrinsic scatter (sig_int)
    sig_int_row = summary_df[summary_df["param"] == "sig_int"]
    sig_int = sig_int_row["mean"].values[0] if not sig_int_row.empty else 0.0

    # Check bounds if recorded in summary
    x_min = summary_df["x_min"].iloc[0]
    x_max = summary_df["x_max"].iloc[0]
    if x_val < x_min or x_val > x_max:
        print(f"Warning: Input x = {x_val} is outside the fitted range [{x_min}, {x_max}]. Extrapolating...")

    # 2. Compute predicted y value: y = sum(a_i * x^i)
    x_powers = np.array([x_val**i for i in range(order + 1)])
    y_pred = np.dot(a_coeffs, x_powers)

    # 3. Compute local derivative (slope dy/dx) for x-error propagation
    if order >= 1:
        deriv_powers = np.array([i * x_val**(i - 1) for i in range(1, order + 1)])
        dy_dx = np.dot(a_coeffs[1:], deriv_powers)
    else:
        dy_dx = 0.0

    # 4. Extract Covariance Matrix for coefficients [a0, ..., an]
    param_names = [f"a{i}" for i in range(order + 1)]
    cov_a = cov_df.loc[param_names, param_names].values

    # 5. Uncertainty Propagation
    var_param = np.dot(x_powers, np.dot(cov_a, x_powers))
    var_x = (dy_dx * x_err_val) ** 2
    var_int = sig_int ** 2

    total_var = var_param + var_x + var_int
    y_err_total = np.sqrt(total_var)

    return {
        "y_pred": y_pred,
        "y_err_total": y_err_total,
        "err_from_parameters": np.sqrt(var_param),
        "err_from_x_uncertainty": np.sqrt(var_x),
        "intrinsic_scatter": sig_int,
    }
#-----------------------------------------------------------------------#


# Main Execution Block
#-----------------------------------------------------------------------#
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Predict dependent variable (y) from fitted summary and covariance matrix from Brooks et al. (in prep.).")
    
    # Parse keyword arguments formatted as key=value
    parser.add_argument("args", nargs="*", help="Arguments in the format key=value (e.g. summary_path=... x=...)")
    parsed_args = parser.parse_args()

    # Convert positional key=value strings into a dictionary
    arg_dict = {}
    for arg in parsed_args.args:
        if "=" in arg:
            key, val = arg.split("=", 1)
            arg_dict[key.strip()] = val.strip()

    summary_path = arg_dict.get("summary_path") or arg_dict.get("summary")
    cov_path = arg_dict.get("cov_path") or arg_dict.get("cov")

    if not summary_path or not cov_path:
        print("Error: Please provide both summary_path and cov_path.")
        print("Usage: python predict_y.py summary_path='path/to/summary.csv' cov_path='path/to/cov.csv' x=2.5 x_err=0.1")
        exit(1)

    # Get x from arguments or prompt if missing
    try:
        if "x" in arg_dict:
            user_x = float(arg_dict["x"])
        else:
            user_x = float(input("Enter independent variable (x value): "))
            
        if "x_err" in arg_dict:
            user_x_err = float(arg_dict["x_err"])
        else:
            user_x_err = float(input("Enter uncertainty in x (x_err value): "))
            
    except ValueError:
        print("Error: Please provide valid numerical values for x and x_err.")
        exit(1)

    try:
        result = predict_dependent_value(user_x, user_x_err, summary_path, cov_path)
        
        print("\n" + "=" * 40)
        print("PREDICTION RESULTS")
        print("=" * 40)
        print(f"Input Independent Variable (x) : {user_x} +/- {user_x_err}")
        print(f"Predicted Dependent Value (y)  : {result['y_pred']:.5e}")
        print(f"Total Relevant Uncertainty (y) : +/- {result['y_err_total']:.5e}")
        print("-" * 40)
        print("Uncertainty Breakdown:")
        print(f"  - Due to model parameters  : {result['err_from_parameters']:.5e}")
        print(f"  - Due to input x-error     : {result['err_from_x_uncertainty']:.5e}")
        print(f"  - Intrinsic scatter (sig)  : {result['intrinsic_scatter']:.5e}")
        print("=" * 40)

    except Exception as e:
        print(f"\nAn error occurred during calculation: {e}")
#-----------------------------------------------------------------------#
