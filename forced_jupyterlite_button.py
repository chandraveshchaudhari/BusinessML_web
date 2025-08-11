import os
import re

# List of allowed notebook files from your TOC (without extension)
toc_files = [
    "symbols",
    "1_Linear_regression",
    "2_Regularization",
    "3_Naive_Bayes",
    "4_Logistic_Regression",
    "5_Dimensionality_Reduction",
    "6_Clustering",
    "7_Gaussian_Mixture_Models",
    "8_Nearest_Neighbour_Algorithm",
    "10_Support_Vector_Machines",
    "11_Decision_Trees",
    "12_Ensemble_Methods",
    "13_Neural_Networks",
    "14_Arima",
    "15_LSTM",
    "16_CNN",
    "17_Resnet",
    "18_LLM",
    "19_Reinforcement_Learning",
    "20_Multimodal_Learning",
    "Generative_Models",
    "Performance_Metrics",
    "Visualization"
]

# Directory containing your built HTML files
html_dir = "docs"

# Regex to find Colab button and extract filename
colab_regex = re.compile(
    r'(<a[^>]+href="https://colab\.research\.google\.com/[^"]+/(?P<filename>[^/"]+\.ipynb)"[^>]*>.*?</a>)',
    re.DOTALL
)

# JupyterLite button template with inline SVG
jupyterlite_template = """
<li>
  <a href="https://chandraveshchaudhari.github.io/BusinessML_web/jupyterlite/lab/index.html?path={filename}" target="_blank"
     class="btn btn-sm dropdown-item"
     title="Launch on JupyterLite"
     data-bs-placement="left" data-bs-toggle="tooltip">
    <span class="btn__icon-container" style="display:inline-block; width:20px; height:20px;">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
        <circle cx="128" cy="128" r="128" fill="#f37726"/>
        <ellipse cx="128" cy="128" rx="110" ry="40" fill="white" transform="rotate(-25, 128, 128)"/>
        <ellipse cx="128" cy="128" rx="110" ry="40" fill="white" transform="rotate(25, 128, 128)"/>
        <circle cx="200" cy="60" r="18" fill="white"/>
        <circle cx="60" cy="200" r="18" fill="white"/>
      </svg>
    </span>
    <span class="btn__text-container">JupyterLite</span>
  </a>
</li>
"""

# Loop through HTML files
for root, _, files in os.walk(html_dir):
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                html = f.read()

            # Search for Colab button
            match = colab_regex.search(html)
            if match:
                filename = match.group("filename")
                notebook_name = filename.replace(".ipynb", "")

                if notebook_name in toc_files:
                    # Build JupyterLite button for this file
                    jl_button = jupyterlite_template.format(filename=filename)

                    # Insert JupyterLite button right after Colab button
                    new_html = html.replace(match.group(1), match.group(1) + "\n" + jl_button)

                    # Save updated HTML
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(new_html)
                    print(f"✅ Added JupyterLite button to {file}")
                else:
                    print(f"⏭ Skipped {file} (not in TOC)")
