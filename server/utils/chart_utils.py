import matplotlib.pyplot as plt
import base64
from io import BytesIO

def dataframe_to_base64_image(df, chart_type="bar", x=None, y=None):
    plt.figure(figsize=(6, 4))

    # Bar chart
    if chart_type == "bar":
        if x and y:
            plt.bar(df[x], df[y])
        else:
            df.plot(kind="bar")
    
    # Line chart
    elif chart_type == "line":
        if x and y:
            plt.plot(df[x], df[y])
        else:
            df.plot(kind="line")

    plt.tight_layout()

    # Convert plot to Base64
    buf = BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)

    img_bytes = buf.getvalue()
    return base64.b64encode(img_bytes).decode("utf-8")
