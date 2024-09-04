from app import app, render_template, session, redirect ,LWork_conn,LWork_cursor,LWork_lock
from flask import jsonify, request, url_for
from datetime import datetime, timedelta, timezone

def GetPermissionsLevel():
    member_id = session.get('UserID')
    LWork_cursor.execute('SELECT PermissionLevel FROM Members WHERE id = ?', (member_id,))
    result = LWork_cursor.fetchone()
    return result[0]

@app.route('/Dev_DBMgr/index')
def Dev_DBMgr():
    if not GetPermissionsLevel():
        return '權限不足'
    with LWork_lock:
        LWork_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = LWork_cursor.fetchall()
        print(tables)
    return render_template('Dev_DBMgr/index.html', tables=tables)



@app.route('/Dev_DBMgr/table/<table_name>')
def table_view(table_name):
    if not GetPermissionsLevel():
        return '權限不足'
    
    LWork_cursor.execute(f"SELECT * FROM {table_name};")
    rows = LWork_cursor.fetchall()
    columns = [description[0] for description in LWork_cursor.description]

    return render_template('/Dev_DBMgr/table_view.html', table_name=table_name, columns=columns, rows=rows)


@app.route('/Dev_DBMgr/table/<table_name>/edit/<int:id>', methods=['GET', 'POST'])
def edit_row(table_name, id):
    if not GetPermissionsLevel():
        return '權限不足'
    
    if request.method == 'POST':
        columns = [description[1] for description in LWork_cursor.execute(f"PRAGMA table_info({table_name})").fetchall()]
        updates = [f"{i} = ?" for i in columns]
        
        values = [request.form[col] for col in columns]
        print(f"UPDATE {table_name} SET {', '.join(updates)} WHERE id = ?", values[0])

        LWork_cursor.execute(f"UPDATE {table_name} SET {', '.join(updates)} WHERE id = {values[0]}", values)
        LWork_conn.commit()
        return redirect(url_for('table_view', table_name=table_name))

    LWork_cursor.execute(f"SELECT * FROM {table_name} WHERE id = ?;", (id,))
    row = LWork_cursor.fetchone()
    columns = [description[0] for description in LWork_cursor.description]
    return render_template('/Dev_DBMgr/edit_row.html', table_name=table_name, row=row, columns=columns)


@app.route('/Dev_DBMgr/table/<table_name>/delete/<int:id>')
def delete_row(table_name, id):
    if not GetPermissionsLevel():
        return '權限不足'
    
    LWork_cursor.execute(f"DELETE FROM {table_name} WHERE id = ?;", (id,))
    LWork_conn.commit()

    return redirect(url_for('table_view', table_name=table_name))