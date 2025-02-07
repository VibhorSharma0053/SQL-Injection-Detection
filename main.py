import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox

def detect_sql_injection(file_path):
    try:
        data = pd.read_csv(file_path)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read file: {str(e)}")
        return

    sql_injection_keywords = [
        "SELECT", "INSERT", "UPDATE", "DELETE", "DROP", "UNION", "WHERE", "HAVING", 
        "JOIN", "ALTER", "EXEC", "' OR '1'='1", "' OR '1'='1' --", "' OR 1=1 --", 
        "' OR 1=1 /*", "' AND 1=2", "' OR TRUE --", "%", "'", '"', ";", "--", 
        "/*", "*/", ":", "' UNION SELECT", "' OR 1=1", "; DROP TABLE", "-- DROP", 
        "' OR ''='", "1=1", "1=0", "CHAR()", "ASCII()", "SLEEP()", "DATABASE()", "VERSION()"
    ]
    
    sp = []
    atkrs = set()
    count = 0
    attacker_id = 'NULL'
    first = 'NULL'
    last = 'NULL'
    f_flag = True

    for index, row in data.iterrows():
        s = str(row['Info'])
        src = str(row['Source'])
        
        for k in sql_injection_keywords:
            if k in s:
                sp.append(src)
                atkrs.add(src)
                break
    
    dic = {at: sp.count(at) for at in atkrs}
    if dic:
        count = max(dic.values())
        attacker_id = max(dic, key=dic.get)
    
    for index, row in data.iterrows():
        s = str(row['Info'])
        src = str(row['Source'])
        
        for k in sql_injection_keywords:
            if k in s and src == attacker_id:
                if f_flag:
                    first = s
                    f_flag = False
                last = s
    
    result_text.set(f"Attacker's IP Address:     {attacker_id}\n\nNo. of SQL Injection Attempts:       {count}\n\nInitial SQL Injection Attempt:     {first}\n\nFinal SQL Injection Attempt:     {last}")

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        detect_sql_injection(file_path)

# GUI Setup
root = tk.Tk()
root.title("SQL Injection Detector")
root.geometry("900x800")

heading = tk.Label(root, text="SQL Injection Detector", font=("Arial", 18))
heading.pack(pady=10)

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(pady=20)

btn_browse = tk.Button(frame, text="Select CSV File", command=browse_file, font=("Arial", 16))
btn_browse.pack()


res = tk.Label(root, text="Result:", font=("Arial", 16))
res.pack(pady=5)


result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text, justify="left", font=("Arial", 12))
result_label.pack(pady=10)

root.mainloop()
