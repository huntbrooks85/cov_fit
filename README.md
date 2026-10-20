<h1 align="center" id="title"> 🧮 cov_fit 🧮 </h1>
<div align="center">

<p id="description"> <b>cov_fit</b> is a tool to use the summary and covariance matrix from Brooks et al. (in prep.) to obtain the dependent variable and uncertainty while considering intrinsic scatter. </p>
</div>

<div align="center">
  <h2>⬇️ PIP Requirements ⬇️</h2>
</div>
<div align="center">
  <p><b></b></p>
</div>

1. ```argparse```
2. ```numpy```
3. ```pandas```

<div align="center">
  <h2>🏆 Using cov_fit 🏆</h2>
</div>

1. Enter directory
2. Enter command: ```python cov_fit.py summary_path="test_summary.csv" cov_path="test_cov.csv" x=20 x_err=0.5```
   1. ```summary_path```: str, input path for the fitted sumary csv.
   2. ```cov_path```:str, input path for the fitted covariance csv.
   3. ```x```: Desired independent variable.
   4. ```x_err```: Desired independent variable unceratiny. 

<div align="center">
  <h2> 🔎 Example 🔍</h2>
</div>

Input: 

```python cov_fit.py summary_path="test_summary.csv" cov_path="test_cov.csv" x=20 x_err=0.5```

Output: 

```
========================================
PREDICTION RESULTS
========================================
Input Independent Variable (x) : 20.0 +/- 0.5
Predicted Dependent Value (y)  : -4.60615e+00
Total Relevant Uncertainty (y) : +/- 1.01092e-01
----------------------------------------
Uncertainty Breakdown:
  - Due to model parameters  : 2.87149e-02
  - Due to input x-error     : 1.94693e-02
  - Intrinsic scatter (sig)  : 9.49527e-02
========================================
```

<div align="center">
  <h2>📞 Support 📞</h2>
</div>

- **Mr. Hunter Brooks**
  - Email: hbrooks8 (at) rockets.utoledo.edu

<div align="center">
  <h2>📖 Acknowledgments 📖</h2>
</div>

<b>Please cite Brook et al. (in prep.) when using cov_fit for any publication.</b>