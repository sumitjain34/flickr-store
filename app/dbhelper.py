from redis import Redis

def save_history(user_ip,search_term):
	try:
		r=Redis()
		r.sadd(user_ip,search_term)
		return True
	except Exception as e:
		return False

def get_history(user_ip):
	r=Redis()
	search_terms=r.smembers(user_ip)
	return list(search_terms)
