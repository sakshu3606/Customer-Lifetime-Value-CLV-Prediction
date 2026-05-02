{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "149088ed-68a5-4ddc-9c00-0dbbcde9a393",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      " * Serving Flask app '__main__'\n",
      " * Debug mode: off\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.\n",
      " * Running on http://127.0.0.1:5000\n",
      "Press CTRL+C to quit\n",
      "127.0.0.1 - - [02/May/2026 15:06:18] \"GET / HTTP/1.1\" 200 -\n",
      "127.0.0.1 - - [02/May/2026 15:06:25] \"POST / HTTP/1.1\" 200 -\n",
      "[2026-05-02 15:07:36,538] ERROR in app: Exception on / [POST]\n",
      "Traceback (most recent call last):\n",
      "  File \"C:\\Users\\saksh\\anaconda3\\Lib\\site-packages\\flask\\app.py\", line 1511, in wsgi_app\n",
      "    response = self.full_dispatch_request()\n",
      "  File \"C:\\Users\\saksh\\anaconda3\\Lib\\site-packages\\flask\\app.py\", line 919, in full_dispatch_request\n",
      "    rv = self.handle_user_exception(e)\n",
      "  File \"C:\\Users\\saksh\\anaconda3\\Lib\\site-packages\\flask\\app.py\", line 917, in full_dispatch_request\n",
      "    rv = self.dispatch_request()\n",
      "  File \"C:\\Users\\saksh\\anaconda3\\Lib\\site-packages\\flask\\app.py\", line 902, in dispatch_request\n",
      "    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)  # type: ignore[no-any-return]\n",
      "           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^\n",
      "  File \"C:\\Users\\saksh\\AppData\\Local\\Temp\\ipykernel_21144\\80600203.py\", line 28, in index\n",
      "    clean_data = preprocess_pipeline.transform(df)\n",
      "  File \"C:\\Users\\saksh\\anaconda3\\Lib\\site-packages\\sklearn\\utils\\_set_output.py\", line 316, in wrapped\n",
      "    data_to_wrap = f(self, X, *args, **kwargs)\n",
      "  File \"C:\\Users\\saksh\\anaconda3\\Lib\\site-packages\\sklearn\\compose\\_column_transformer.py\", line 1088, in transform\n",
      "    raise ValueError(f\"columns are missing: {diff}\")\n",
      "ValueError: columns are missing: {'age', 'avg_order_value', 'last_purchase_value', 'frequency_orders', 'email_click_rate', 'satisfaction_score', 'churn_risk', 'loyalty_points', 'last_login_days', 'avg_session_time', 'gender', 'tenure_months', 'customer_segment', 'city', 'payment_method', 'referral_count', 'max_order_value', 'region', 'recency_days', 'app_visits_per_month', 'returns_count', 'product_category', 'customer_id', 'complaints', 'total_spent', 'discount_usage', 'min_order_value'}\n",
      "127.0.0.1 - - [02/May/2026 15:07:36] \"POST / HTTP/1.1\" 500 -\n",
      "127.0.0.1 - - [02/May/2026 15:07:42] \"POST / HTTP/1.1\" 200 -\n"
     ]
    }
   ],
   "source": [
    "from flask import Flask, render_template, request\n",
    "import pandas as pd\n",
    "import joblib\n",
    "import os\n",
    "\n",
    "app = Flask(__name__)\n",
    "\n",
    "# Load model and preprocessing pipeline\n",
    "model = joblib.load(\"xgboost.pkl\")\n",
    "preprocess_pipeline = joblib.load(\"xgboost_preprocess_pipeline.pkl\")\n",
    "\n",
    "@app.route(\"/\", methods=[\"GET\", \"POST\"])\n",
    "def index():\n",
    "    output = None\n",
    "\n",
    "    if request.method == \"POST\":\n",
    "        file = request.files[\"file\"]\n",
    "\n",
    "        if file.filename.endswith(\".csv\"):\n",
    "            df = pd.read_csv(file)\n",
    "        elif file.filename.endswith(\".xlsx\"):\n",
    "            df = pd.read_excel(file)\n",
    "        else:\n",
    "            output = \"Please upload only CSV or Excel file.\"\n",
    "            return render_template(\"index.html\", output=output)\n",
    "\n",
    "        # Preprocess data\n",
    "        clean_data = preprocess_pipeline.transform(df)\n",
    "\n",
    "        # Prediction\n",
    "        predictions = model.predict(clean_data)\n",
    "\n",
    "        df[\"Predicted_CLV\"] = predictions\n",
    "\n",
    "        output = df.to_html(index=False)\n",
    "\n",
    "    return render_template(\"index.html\", output=output)\n",
    "\n",
    "if __name__ == \"__main__\":\n",
    "    app.run(debug=False, use_reloader=False)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.13.9"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
