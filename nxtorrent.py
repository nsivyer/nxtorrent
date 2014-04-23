#!/usr/bin/env python
import libtorrent as lt
import time,os,sys,getopt,threading


class ntorrent:

	directory=''
	ses=None
	tick_interval=1
	torrents={}
	processed_torrents={}
	execute=False
	state_str = ['queued', 'checking', 'downloading metadata', \
		'downloading', 'finished', 'seeding', 'allocating', 'checking fastresume']

	def parse_args(self):
		help_text = "ntorrent.py -d <directory> -p <port> [-x]"
		if len(sys.argv[1:]) < 1:
			print help_text
			sys.exit(1)
		try:
			opts, args = getopt.getopt(sys.argv[1:],"d:p:x", ["help"])
		except getopt.GetoptError:
			print help_text
			sys.exit(2)

		for opt, arg in opts:
			if opt == '--help':
				print help_text
				sys.exit()
			elif opt in ("-d"):
				if not os.path.isdir(arg):
					print arg + " is not a directory"
					exit(2)
				self.directory = arg
			elif opt in ("-p"):
				self.port = int(arg)
			elif opt in ("-x"):
				self.execute = True
			else:
				print help_text
				exit(2)

	def create_session(self):
		self.ses = lt.session()
		self.ses.listen_on(self.port,self.port+10)
		#self.ses.start_dht()

   	def print_line(self,line):
   		print(line+"\n")
   		sys.stdout.flush()

   	def remove_torrent(self,filename):
		self.print_line("Remove " + filename)
		self.ses.remove_torrent(self.torrents[filename])
		del self.torrents[filename]
		if filename in self.processed_torrents.keys():
			del self.processed_torrents[filename]


	def start_torrent(self,filename):
		self.print_line("Adding " + filename)
		e = lt.bdecode(open(filename, 'rb').read())
		info = lt.torrent_info(e)
		h = self.ses.add_torrent(info, "./")
		self.torrents[filename] = h

	def finish_torrent(self,torrent):
		self.print_line("Finished " + torrent)
		if torrent not in self.processed_torrents.keys():
			t=self.torrents[torrent]
			self.processed_torrents[torrent] = self.torrents[torrent]
			num_of_files=t.get_torrent_info().num_files()
			#check to see what the payload is
			if num_of_files == 1 and self.execute:
				file_path=t.get_torrent_info().file_at(0).path
				full_file_path = self.directory + "/" + file_path
				self.print_line("Trying to run " + full_file_path)
				if not os.path.isfile(full_file_path):
					self.print_line("File Missing or directory error! - " + full_file_path)
					return
				else:
					os.system("/bin/sh -x "+self.directory + "/" + file_path)
					self.print_line("Done")

		#run file
		#delete file?
		#remove from list

	def print_stats(self):
		for x in self.torrents.keys():
			s = self.torrents[x].status()
			status = self.state_str[s.state]
			if status == "seeding" and x not in self.processed_torrents.keys():
				self.finish_torrent(x)
			print('%.2f%% complete - %s (down: %.1f kb/s up: %.1f kB/s peers: %d) %s' % (s.progress * 100, x, s.download_rate / 1000, s.upload_rate / 1000, s.num_peers, self.state_str[s.state]))
			sys.stdout.flush()
		#print("\n")

	def tick(self):
		self.print_stats()
		#scan dir
		for filename in os.listdir(self.directory):
			if filename.endswith(".torrent"):
				f=self.directory+'/'+filename
				if f not in self.torrents:
					self.start_torrent(f)
		for t in self.torrents:
			if not os.path.isfile(t):
				self.remove_torrent(t)
				return

	def run(self):
		while True:
			self.tick()
			time.sleep(ntorrent.tick_interval)

	def is_exe(self,fpath):
		return os.path.isfile(fpath) and os.access(fpath, os.X_OK)


if __name__ == "__main__":

    ntorrent = ntorrent()
    ntorrent.parse_args()
    ntorrent.create_session()
    ntorrent.run()






