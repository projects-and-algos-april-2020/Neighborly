from config import app
from controller import index, add_user, login, logout


app.add_url_rule("/", view_func=index)
app.add_url_rule("/process/user", view_func=add_user, methods=['POST'])
app.add_url_rule("/login", view_func=login, methods=['POST'])
app.add_url_rule("/logout", view_func=logout)

