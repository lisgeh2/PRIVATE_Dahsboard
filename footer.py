from html import escape
import base64


def footer(logos=None):
    # Load and encode logo images
    logo_html = ""
    if logos:
        for logo_path in logos:
            try:
                with open(logo_path, "rb") as f:
                    logo_b64 = base64.b64encode(f.read()).decode("utf-8")
                    logo_alt = escape(logo_path.replace(".png", "").replace("_", " ").title())
                    logo_html += f'<img src="data:image/png;base64,{logo_b64}" alt="{logo_alt}">\n'
            except FileNotFoundError:
                continue

    return f"""
<footer>
  <div class="container">
    <div class="footer-logos">
      {logo_html}
    </div>
  </div>
</footer>
"""