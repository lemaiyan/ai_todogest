EMAIL_HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
        }}
        .container {{
            max-width: 600px;
            margin: 20px auto;
            background-color: #ffffff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }}
        .header {{
            text-align: center;
            padding: 20px 0;
        }}
        .header h1 {{
            margin: 0;
            color: #333333;
        }}
        .content {{
            padding: 20px 0;
        }}
        .content p {{
            color: #555555;
            line-height: 1.6;
        }}
        .email-entry {{
            margin-bottom: 20px;
            padding: 10px;
            border-left: 3px solid #0078d7;
            background-color: #f9f9f9;
        }}
        .footer {{
            text-align: center;
            padding: 10px 0;
            color: #888888;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Email Digest</h1>
        </div>
        <div class="content">
            {email_summaries}
        </div>
        <div class="footer">
            <p>TodoGest. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
"""