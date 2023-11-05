import streamlit as st
import re
import os

#api:
#localhost:4000/?file=README.md
#st.experimental_set_query_params(show_map=True,selected=["asia", "america"],)
#st.experimental_get_query_params()
#{"show_map": ["True"], "selected": ["asia", "america"]}



def find_menu(fr):
	matches = list(re.findall(r"(\#{1,6}\s+([^\r\n]+))", fr))
	for i in range(len(matches)):
		matches[i] = list(matches[i])
		matches[i][0] = matches[i][0].count('#')
	#hmatches = matches[:]
	hmatches = []
    
	for i in range(len(matches)):
		hmatches.append(matches[i][:])
	for i in range(len(hmatches)):
		hmatches[i][1] = re.sub(r'([0-9]+)',r"-\1-", hmatches[i][1])
		hmatches[i][1] = re.sub(r"(\W+)", r"-", hmatches[i][1])
		hmatches[i][1] = re.sub(r"^-|-$", r"", hmatches[i][1])
	return matches, hmatches

def find_dir():
	tree = []
	for root, dirs, files in os.walk('.'):
		for file in files:
			tree.append(os.path.join(root, file))
	otree = tree[:]
	#print(otree)
	tree = []
	for i in range(len(otree)):
		if otree[i].endswith('.md'):
			tree.append(otree[i])
	utree = tree[:]
	for i in range(len(utree)):
		utree[i] = utree[i].replace(' ','%20')
	return tree,utree


url_q = st.experimental_get_query_params()
if url_q == {}:
	raise IOError
with open(url_q['file'][0],'r',encoding='utf-8') as file:
	file_read = file.read()
	file_readline = file.readline()

sbs = st.sidebar.selectbox('侧栏sidebar：',('章节chapters','文件目录dir'))
if sbs:
	if sbs == '章节chapters':
		rt_menu = find_menu(file_read)[0]
		rt_hmenu = find_menu(file_read)[1]
		for i in range(len(rt_menu)):
			st.sidebar.markdown('-| ' * rt_menu[i][0] + f"[{rt_menu[i][1]}](#{rt_hmenu[i][1]})")
	elif sbs == '文件目录dir':
		rt_dir = find_dir()[0]
		rt_udir = find_dir()[1]
		#print(rt_dir)
		#print(rt_udir)
		for i in range(len(rt_dir)):
			st.sidebar.markdown(f"[{rt_dir[i]}](/?file={rt_udir[i]})")
	else:
		print('???')

st.markdown(file_read)


