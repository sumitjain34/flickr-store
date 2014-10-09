def solve_pagination(total_pages,page_no):
	print "solving pagination"
	if page_no > 5 and page_no != total_pages:
		start_page = page_no - 4
		end_page = start_page + 9
	elif page_no <= 5:
		start_page = 1
		end_page = start_page + 9
	else:
		end_page = total_pages
		start_page = total_pages - 9
	if end_page > total_pages and end_page != total_pages:
		end_page = total_pages
		start_page = total_pages - 9
	if start_page < 0:
		start_page = 1
		end_page = total_pages
	return [start_page,end_page]
