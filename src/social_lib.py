from requests import Session

class SocialLib:
	def __init__(self) -> None:
		self.api = "https://lib.social"
		self.session = Session()
		self.session.headers = {
			"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36"
		}
		self.csrf_token = self.get_csrf_token()["csrf"]

	def get_csrf_token(self) -> dict:
		return self.session.get(
			f"{self.api}/_refresh-token").json()

	def upload_image(self, file: bytes) -> dict:
		files = {
			"file": ("image.jpg", file, "image/jpeg")
		}
		return self.session.post(
			f"{self.api}/upload/image", files=files).json()
	
	def login_with_web_token(self, remember_web: str) -> str:
		self.remember_web = remember_web
		self.session.headers["cookie"] = self.remember_web
		return remember_web
		
	def reset_password(
			self,
			email: str,
			password: str,
			token: str) -> dict:
		data = {
			"_token": self.csrf_token,
			"token": token,
			"email": email,
			"password": password,
			"password_confirmation": password
		}
		return self.session.post(
			f"{self.api}/password/reset", data=data).json()

	def chat_auth(self, auth: bool = True) -> dict:
		return self.session.get(
			f"{self.api}/chat?auth={auth}").json()

	def get_chat_message(self, message_id: int) -> dict:
		return self.session.get(
			"{self.api}/message?id={message_id}").json()

	def change_password(
			self,
			old_password: str,
			new_password: str) -> dict:
		data = {
			"_token": self.csrf_token,
			"old_password": old_password,
			"new_password": new_password,
			"new_password_confirmation": new_password
		}
		return self.session.post(
			f"{self.api}/settings/password?{self.user_id}",
			data=data).json()

	def get_notifications(
			self,
			page: int = 1,
			type: str = "all",
			ajax: bool = True,
			get_counts: bool = True) -> dict:
		return self.session.get(
			f"{self.api}notification?page={page}&type={type}&ajax={ajax}&getCounts={get_counts}").json()

	def get_user_bookmark(self, user_id: int) -> dict:
		return self.session.get(
			f"{self.api}/bookmark/{user_id}").json()

	def follow_user(self, user_id: int) -> dict:
		data = {
			"follower_id": user_id
		}
		return self.session.post(
			f"{self.api}/follow", data=data).json()

	def block_user(self, user_id: int) -> dict:
		data = {
			"block_id": user_id
		}
		return self.session.post(
			f"{self.api}/block", data=data).json()

	def get_discussions(
			self,
			category: str = "all",
			subscription: int = 0,
			page: int = 1,
			sort: str = "newest") -> dict:
		return self.session.get(
			f"{self.api}/api/forum/discussion?category={category}&subscription={subscription}&page={page}&sort={sort}").json()

	def search_discussion(
			self,
			title: str,
			category: str = "all",
			subscription: int = 0,
			page: int = 1,
			sort: str = "newest") -> dict:
		return self.session.get(
			f"{self.api}/api/forum/discussion?category={category}&title={title}&subscription={subscription}&page={page}&sort={sort}").json()

	def get_user_discussions(
			self,
			user_id: int,
			subscription: int = 0,
			page: int = 1,
			sort: str = "newest") -> dict:
		return self.session.get(
			f"{self.api}/api/forum/discussion?user_id={user_id}&subscription={subscription}&page={page}&sort={sort}").json()

	def get_subscriptions(
			self,
			page: int = 1,
			sort: str = "newest") -> dict:
		return self.session.get(
			f"{self.api}/api/forum/discussion?subscription=1&page={page}&sort={sort}").json()

	def follow_discussion(self, discussion_id: int) -> dict:
		return self.session.post(
			f"{self.api}/api/forum/discussion/{discussion_id}/notification").json()

	def comment_discussion(self, discussion_id: int, text: str) -> dict:
		data = {
			"body": {
				"ops": [
					{
						"insert": text
					}
				]
			},
			"chatter_discussion_id": discussion_id
		}
		return self.session.post(
			f"{self.api}/api/forum/posts", data=data).json()

	def check_chat_online(self, users: list) -> dict:
		data = {
			"users": users
		}
		return self.session.post(
			f"{self.api}/chat/check-online", data=data).json()

	def search_user(self, query: str) -> dict:
		return self.session.get(
			f"{self.api}/search?type=user&q={query}").json()

	def get_updates(self, page: int = 1) -> dict:
		return self.session.get(
			f"{self.api}/user/updates?page={page}").json()

	def send_message(self, text: str, before: int) -> dict:
		data = {
			"text": text,
			"before": before
		}
		return self.session.post(
			f"{self.api}/chat", data=data).json()

	def edit_profile(
			self,
			username: str = None,
			email: str = None,
			gender: int = 0,
			about: str = None) -> dict:
		data = {
			"_token": self.csrf_token,
			"gender": gender,
			"username": username,
			"email": email,
			"about": about
		}
		filtered_data = {
			key: value for key, value in data.items() if value is not None
		}
		return self.session.post(
			f"{self.api}/user/{self.user_id}/save",
			data=filtered_data).json()

	def edit_comment(
			self,
			comment_id: int,
			text: str) -> dict:
		data = {
			"body": {
				"ops": [
					{
						"insert": text
					}
				]
			}
		}
		return self.session.put(
			f"{self.api}/api/forum/posts/{comment_id}", data=data).json()

	def delete_comment(
			self,
			discussion_id: int,
			post_ids: list) -> dict:
		data = {
			"postIds": post_ids,
			"chatter_discussion_id": discussion_id
		}
		return self.session.delete(
			f"{self.api}/api/forum/posts", data=data).json()

	def get_discussion(self, discussion_id: int) -> dict:
		return self.session.get(
			f"{self.api}/api/forum/discussion/{discussion_id}").json()

	def lock_discussion(self, discussion_id: int) -> dict:
		data = {
			"actionType": "locked"
		}
		return self.session.post(
			f"{self.api}/api/forum/discussion/{discussion_id}/action",
			data=data).json()

	def create_discussion(
			self, 
			title: str, 
			description: str, 
			category_id: int,
			yaoi: bool = False,
			image: str = None) -> dict:
		data = {
			"title": title,
			"body": {
				"ops": [
					{
						"insert": {
							"image": {
								"src": "https://lib.social/forum/undefined",
								"width": 0,
								"height": 0
							}
						}
					},
				{
					"insert": description
				}
			]
		},
		"chatter_category_id": category_id,
		"yaoi": yaoi
		}
		if image:
			data["body"]["ops"][0]["insert"]["image"]["src"] = image
		return self.session.post(
			f"{self.api}/api/forum/discussion", data=data).json()
			
