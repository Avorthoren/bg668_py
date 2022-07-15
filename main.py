import time
import requests
import chess.syzygy


def check_online(fen, request_delay=0):
	time.sleep(request_delay)

	url = "http://tablebase.lichess.ovh/standard/mainline"
	fen_tail = "_b_-_-_0_1"
	response = requests.get(url=url, params={"fen": fen + fen_tail})
	data = response.json()

	return data.get("winner") == "w"


def check(fen, tablebase):
	fen_tail = " b - - 0 1"
	board = chess.Board(fen + fen_tail)
	return tablebase.probe_wdl(board) == -2


with open('positions_all_p6.txt') as input_file:

	fen_cnt = 0
	fen_cnt_last = 0
	fen_cnt_max = 1000000000

	kcnt = 0
	klcnt = 0

	fen = input_file.readline()
	while fen and fen_cnt < fen_cnt_last and fen_cnt < fen_cnt_max:
		fen_cnt += 1
		fen = input_file.readline()

	win_cnt = 0

	with chess.syzygy.open_tablebase(
			"/home/undef/PycharmProjects/BG668/syzygy"
	) as tablebase:
		with open('positions_win_p6.txt', 'a' if fen_cnt_last else 'w') as output_file:
			while fen and fen_cnt < fen_cnt_max:
				fen_cnt += 1
				fen = fen[:-1]

				klcnt += 1
				if klcnt == 1000:
					kcnt += 1
					klcnt = 0
					print(f"\r{kcnt}k ({win_cnt}): {fen}", end="     ")

				# white_win = check_online(fen, request_delay=0.5)
				white_win = check(fen, tablebase)
				if white_win:
					win_cnt += 1
					print(f"\r{fen_cnt}: {fen}       ")
					output_file.write(f"{fen_cnt}: {fen}\n")

				fen = input_file.readline()
