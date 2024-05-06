import os
import json
import hashlib
import shutil

base = os.path.dirname(os.path.abspath(__file__))

# config
manifest_path = os.path.join(base, 'server-manifest.json')
override_path = os.path.join(base, 'overrides')

detect_base = os.path.abspath('/Users/muyunxi/Desktop/desktop/Minecraft/minecraft/versions/TC3')
override_contents = [
	'mods',
	'config/xaerominimap.txt',
	'config/oreexcavation-common.toml',
	'resourcepacks/Minecraft-Mod-Language-Modpack-Converted-1.18.2.zip',
	'hmclversion.cfg'
]

override_ignore = [
	'.DS_Store',
	'desktop.ini',
	'System Volume Information',
	'Thumbs.db',
	'$RECYCLE.BIN',
	'.hmcl.json',
	'.config.ini',
	'autorun.inf'
]

manifest = {
	"name": "Tinkers-Construct",
	"author": "Iewnfod",
	"version": "1.18.2a7",
	"description": "",
	"fileApi": "https://github.createchstudio.com/https://github.com/CreatechStudio/Tinkers-Construct/blob/main",
	"files": {},
	"addons": [
		{
			"id": "game",
			"version": "1.18.2"
		},
		{
			"id": "forge",
			"version": "40.2.18"
		}
	],
}

# funcs
def get_hash(p):
	sha1 = hashlib.sha1()
	with open(p, 'rb') as f:
		while True:
			data_bytes = f.read(128000)
			sha1.update(data_bytes)
			if not data_bytes:
				break
	return sha1.hexdigest()

def copy_file(original_path, p):
	shutil.copyfile(original_path, os.path.join(override_path, p))

def scan_dir(content_path, p):
	files = []

	current_override_path = os.path.join(override_path, p)

	if not os.path.exists(current_override_path):
		os.mkdir(current_override_path)

	for _p, dir_list, file_list in os.walk(content_path):
		for d in dir_list:
			if d in override_ignore:
				continue
			files += scan_dir(os.path.join(content_path, d), os.path.join(p, d))
		for f in file_list:
			if f in override_ignore:
				continue
			files.append({
				'path': os.path.join(p, f),
				'hash': get_hash(os.path.join(_p, f))
			})
			copy_file(os.path.join(content_path, f), os.path.join(p, f))

	return files

def new_files():
	files = []

	if not os.path.exists(override_path):
		os.mkdir(override_path)

	for content in override_contents:
		if content in override_ignore:
			continue

		content_path = os.path.join(detect_base, content)
		if os.path.exists(content_path):
			if os.path.isdir(content_path):
				files += scan_dir(content_path, content)
			elif os.path.isfile(content_path):
				files.append({
					'path': content,
					'hash': get_hash(content_path)
				})
				parent_dir = os.path.dirname(os.path.join(override_path, content))
				if not os.path.exists(parent_dir):
					os.mkdir(parent_dir)
				copy_file(content_path, content)

	return files

# main
manifest['files'] = new_files()

with open(manifest_path, 'w') as f:
	f.write(json.dumps(manifest, indent=2))