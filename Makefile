run:
	python3 weibo.py
	python3 zhihu.py
	python3 rss.py

clean-data:
	git restore --staged --worktree data/*