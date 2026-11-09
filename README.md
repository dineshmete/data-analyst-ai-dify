# Data Analyst AI Agent (Dify)

A Dify AI agent that answers questions about an uploaded CSV file. Upload the file once, then ask many questions in the same chat. The agent uses tools to run calculations with a Code Interpreter, draw ECharts charts, check the data for mismatches, and send the summary by Gmail after the user confirms.

Tested on a 10-row sales dataset (`sales.csv`).

## Workflow

Start → IF-ELSE → Doc Extractor → Variable Assigner → Code → Agent → Answer

1. **Start:** `user_file` (File List) and `sys.query`.
2. **IF-ELSE:** if `user_file` is not empty, read it. Otherwise use the file saved earlier in the chat.
3. **Doc Extractor:** turns the CSV into text.
4. **Variable Assigner:** saves the text to the conversation variable `csv_data`.
5. **Code:** `code_node.py` builds a summary: row count, overall sums, averages, min, max, group totals, and a data check (TotalSales = Quantity × UnitPrice).
6. **Agent:** Function Calling, memory on (window 10), maximum iterations 10. Tools: ECharts Linear, Bar and Pie charts, Code Interpreter, and Gmail Send Message. The instruction is in `agent_prompt.txt`.
7. **Answer:** shows the Agent's text.

## Setup

1. Create a Chatflow app in Dify.
2. Add `user_file` (File List) to the Start node.
3. Add the IF-ELSE node and the Doc Extractor, Variable Assigner and Code nodes as above.
4. Create the conversation variable `csv_data` (Array[String]).
5. Paste `code_node.py` into the Code node. Input `csv_text` = `csv_data`. Output `summary` (String).
6. Add the Agent node with the tools listed above. Paste `agent_prompt.txt` as the instruction.
7. For Gmail, create a Google OAuth client (Web application), add the Dify redirect URI, add your Gmail as a test user, and authorize it in Dify. Never put the Client ID or Secret in this repo.

## Test results

| Question | Result |
|---|---|
| Total sales | 34,228 |
| Total units | 72 |
| Average order value | 3,422.80 |
| Category totals | Clothing 14,971, Electronics 12,982, Groceries 6,275 |
| Region totals | North 10,089, South 9,776, East 9,882, West 4,481 |
| Electronics average TotalSales | 3,245.50 |
| Clothing orders with quantity above 10 | 1 |
| Highest quantity order | OrderID 108 (15) |
| Data check | 1 mismatch: OrderID 105, expected 4,796, recorded 4,996 |
| Charts | Bar, pie and quantity charts pass |
| Email | Sent only after explicit confirmation |

## Limitations

- The model is Auto Router on the free tier, so answers can vary between runs. A fixed paid model is planned.
- The Code Interpreter sometimes sends an empty call and fails. Calculation questions can then fail, while summary-based answers still work.
- The sandbox has only the Python standard library (no pandas). The CSV text is pasted into the code, so only small files are practical.
- Only the TotalSales = Quantity × UnitPrice check is built in.
- Charts are bar, line and pie only. The Dify chat cannot show a custom dashboard.
- Tested on one 10-row file.

## Next steps

1. Use a paid API key and a fixed model, then run all tests again.
2. Re-test calculation questions after the model is fixed.
3. Test with larger and multiple CSV files.
4. Add CSV or Excel export.

## Also in this repo

- `sales-dashboard/sales_dashboard.html`: a separate HTML dashboard with KPI cards, category and region slicers, and charts. It is hardcoded to `sales.csv`. It loads Chart.js from cdnjs, so it needs internet.
- `screenshots/`: workflow, chat, agent settings and instruction.
