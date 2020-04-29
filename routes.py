from config import app
from controller import index, add_user, login, logout, register, user_profile, dashboard, add_post, events, add_event, event_details, add_event_comments, edit_event, update_event, delete_event, delete_post, like_post, like_count


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
app.add_url_rule("/event/details/<event_id>", view_func=event_details)
app.add_url_rule("/add/event_comment/<event_id>", view_func=add_event_comments, methods=['POST'])
app.add_url_rule("/edit/event/<event_id>", view_func=edit_event)
app.add_url_rule("/update/event/<event_id>", view_func=update_event, methods=['POST'])
app.add_url_rule("/delete/event/<event_id>", view_func=delete_event)
app.add_url_rule("/delete/post/<post_id>", view_func=delete_post)
app.add_url_rule("/like/post/<post_id>", view_func=like_post)
app.add_url_rule("/like/count/<post_id>", view_func=like_count)