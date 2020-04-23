from config import app
from controller import index, add_user, login, logout, register, user_profile, dashboard, add_post, events, add_event


app.add_url_rule("/", view_func=index)
app.add_url_rule("/register", view_func=register)
app.add_url_rule("/process/user", view_func=add_user, methods=['POST'])
app.add_url_rule("/login", view_func=login, methods=['POST'])
app.add_url_rule("/logout", view_func=logout)
app.add_url_rule("/user_profile", view_func=user_profile)
app.add_url_rule("/dashboard", view_func=dashboard)
app.add_url_rule("/add/post", view_func=add_post, methods=['POST'])
app.add_url_rule("/events", view_func=events)
app.add_url_rule("/add/event", view_func=add_event, methods=['POST'])