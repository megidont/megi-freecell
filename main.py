##imports

import random;
from colorama import init;
import re;
import os;
import sys;
import math;

##Borrowed functions

def esc(code: str):		#repurposed from code by Christopher Trudeau
    return "\033[" + code + "m"

##Constants

SUIT_SPADES =	0b01000000;
SUIT_HEARTS =	0b01010000;
SUIT_CLUBS =	0b01100000;
SUIT_DIAMONDS =	0b01110000;

SUITS =		[
			0b01000000,
			0b01010000,
			0b01100000,
			0b01110000
		]

SUITMASK =	0b11110000;
VALUMASK =	0b00001111;
REDMASK  =	0b00010000;

SPADESCOMPLETE		= "L";
HEARTSCOMPLETE		= "\\";
CLUBSCOMPLETE		= "l";
DIAMONDSCOMPLETE	= "|";

shufflecount = 7;
playmode = 1;

cellColours = {
	"1" : esc("30;42"),
	"2" : esc("30;42"),
	"3" : esc("30;42"),
	"4" : esc("30;42"),
	"5" : esc("30;42"),
	"6" : esc("30;42"),
	"7" : esc("30;42"),
	"8" : esc("30;42"),
	"Q" : esc("31;40"),
	"W" : esc("32;40"),
	"E" : esc("34;40"),
	"R" : esc("33;40"),
	"S" : esc("30;47"),
	"H" : esc("31;47"),
	"C" : esc("30;47"),
	"D" : esc("31;47")
}

##Card Functions

def makeCard(suit: int, val: int) -> int:
	return (suit & SUITMASK) + (val & VALUMASK);

def getCardInfo(card: int) -> tuple[int]:
	return (card & SUITMASK, card & VALUMASK);

def cardSymbol(card: int) -> str:
	suit = card & SUITMASK;
	valu = card & VALUMASK;
	resstring = "";
	match valu:
		case 0x00:
			resstring = "A";
		case 0x09:
			resstring = "T";
		case 0x0A:
			resstring = "J";
		case 0x0B:
			resstring = "Q";
		case 0x0C:
			resstring = "K";
		case default:
			resstring = str(valu + 1);

	match suit:
		case 0x40:
			resstring += "♠";
		case 0x50:
			resstring += "♥";
		case 0x60:
			resstring += "♣";
		case 0x70:
			resstring += "♦";
		case default:
			resstring = "  ";
	return resstring;

def cardName(card: int) -> str:
	suit = card & SUITMASK;
	valu = card & VALUMASK;
	resstring = "";
	match valu:
		case 0x00:
			resstring = "Ace of ";
		case 0x0A:
			resstring = "Jack of ";
		case 0x0B:
			resstring = "Queen of ";
		case 0x0C:
			resstring = "King of ";
		case default:
			resstring = str(valu + 1) + " of ";

	match suit:
		case 0x40:
			resstring += "Spades";
		case 0x50:
			resstring += "Hearts";
		case 0x60:
			resstring += "Clubs";
		case 0x70:
			resstring += "Diamonds";
		case default:
			resstring = "Joker";
	return resstring;

##Deck Functions

def makeDeck(deckstring = "@ABCDEFGHIJKLPQRSTUVWXYZ[\`abcdefghijklpqrstuvwxyz{|") -> list[int]:
	j = 0;
	if deckstring is None:
		deckstring = "@ABCDEFGHIJKLPQRSTUVWXYZ[\`abcdefghijklpqrstuvwxyz{|";
	deck = [0]*len(deckstring);
	for letter in list(deckstring):
		deck[j] = ord(letter);
		j += 1;

	return deck;

def deckString(deck: list[int]) -> str:
	j = 0;
	k = len(deck);
	deckstring = "";
	while j < k:
		deckstring += chr(deck[j]);
		j += 1;
	return deckstring;

def drawCard(deck: list[int]) -> int:
	if len(deck) == 0:
		return makeCard(0, 13);
	return deck.pop();

def drawCards(deck: list[int], count: int) -> list[int]:
	i = count;
	pile = [];
	while i > 0:
		pile.append(drawCard(deck));
		i -= 1;
	return pile;

def shuffle(deck: list[int]) -> list[int]:
	random.shuffle(deck);
	return deck;

def riffleShuffle(deck: list[int], iterations: int) -> list[int]:
	while iterations > 0:
		height = len(deck);
		halfHeight = height // 2;
		deckstring = deckString(deck);
		lowerHalf = "";
		upperHalf = "";
		r = random.randint(0,1);
		if r == 1:
			lowerHalf = deckstring[:halfHeight];
			upperHalf = deckstring[halfHeight:];
		else:
			lowerHalf = deckstring[halfHeight:];
			upperHalf = deckstring[:halfHeight];
		runoff = 0;
		wholeString = "";
		while len(upperHalf) > 1:
			j = random.randint(0, 1);
			runoff += j;
			wholeString += upperHalf[:j + 1];
			upperHalf = upperHalf[j+1:];
			wholeString += lowerHalf[0];
			lowerHalf = lowerHalf[1:]
		for letter in lowerHalf:
			wholeString += letter;
		if len(upperHalf) == 1:
			wholeString += upperHalf[0];
		deck = makeDeck(wholeString);

		iterations -= 1;
	return deck;

##Game functions

def dealBoard(deck: list[int]) -> dict:
	pileheight = math.floor((len(deckString(deck)) + 1)/8);
	heightoff = (len(deckString(deck)) + 1) % 8;
	return {
		"1" : deckString(drawCards(deck, pileheight + (1 if heightoff > 1 else 0))),
		"2" : deckString(drawCards(deck, pileheight + (1 if heightoff > 2 else 0))),
		"3" : deckString(drawCards(deck, pileheight + (1 if heightoff > 3 else 0))),
		"4" : deckString(drawCards(deck, pileheight + (1 if heightoff > 4 else 0))),
		"5" : deckString(drawCards(deck, pileheight + (1 if heightoff > 5 else 0))),
		"6" : deckString(drawCards(deck, pileheight + (1 if heightoff > 6 else 0))),
		"7" : deckString(drawCards(deck, pileheight + (1 if heightoff > 7 else 0))),
		"8" : deckString(drawCards(deck, pileheight)),
		"Q":"",
		"W":"",
		"E":"",
		"R":"",
		"S":"",
		"H":"",
		"C":"",
		"D":""
	}

def boardString(b: dict[str, str]) -> str:
	bs = "";
	cellList = [ "Q", "W", "E", "R", "S", "H", "C", "D"];
	columnList = [ "1", "2", "3", "4", "5", "6", "7", "8"];
	for k in cellList:
		if list(b[k]) != []:
			bs += cardSymbol(ord(list(b[k])[0]));
		else:
			bs += "  ";
		if k == "4":
			bs += " ¦ ";
		elif k != "D":
			bs += " | ";
		else:
			bs += " \n";
	bs += "--------------------------------------\n";
	rows = ["   |    |    |    ¦    |    |    |    \n"] * 19;
	i = 0;
	while i < 8:
		column = b[columnList[i]];
		j = 0;
		while j < len(column):
			rows[j] = rows[j][:5 * i] + cardSymbol(ord(column[j])) + rows[j][(5 * i) + 2:];
			j += 1;
		i += 1;
	for row in rows:
		if row == "   |    |    |    ¦    |    |    |    \n":
			break;
		bs += row;
	return bs;

def selectCard(b: dict[str, str], c: str) -> int:
	if b[c[0]] == "":
		return 0;
	return ord(b[c[0]][-1]);

def makeMove(move: str, b: dict[str, str]) -> int:
	move = move.upper();
	returncode = 0;
	validList = ["Q", "W", "E", "R", "S", "H", "C", "D", "1", "2", "3", "4", "5", "6", "7", "8"];
	if (move[0] not in validList) or (move[1] not in validList):
		returncode = 1;
		return returncode;

	srcCard = selectCard(b, move[0]);
	destCard = selectCard(b, move[1]);
	srcCardSuit = srcCard & SUITMASK;
	srcCardValu = srcCard & VALUMASK;
	destCardSuit = destCard & SUITMASK;
	destCardValu = destCard & VALUMASK;

	if srcCard == 0:
		returncode = 6;
		return returncode;
	if destCard == 0:
		if move[1] in ("Q", "W", "E", "R"):
			b[move[1]] = chr(srcCard);
			if move[0] in ("Q", "W", "E", "R"):
				b[move[0]] = "";
			elif move[0] in ("S", "H", "C", "D"):
				b[move[0]] = chr(srcCard - 1);
			else:
				b[move[0]] = b[move[0]][:-1];
			returncode = 0;
			return returncode;
		if move[1] in ("S", "H", "C", "D"):
			if srcCardValu != 0:
				returncode = 2;
				return returncode;
			b[move[1]] = chr(srcCard);
			if move[0] in ("Q", "W", "E", "R"):
				b[move[0]] = "";
			elif move[0] in ("S", "H", "C", "D"):
				b[move[0]] = chr(srcCard - 1);
			else:
				b[move[0]] = b[move[0]][:-1];
			returncode = 0;
			return returncode;
		b[move[1]] = chr(srcCard);
		if move[0] in ("Q", "W", "E", "R"):
			b[move[0]] = "";
		elif move[0] in ("S", "H", "C", "D"):
			b[move[0]] = chr(srcCard - 1);
		else:
			b[move[0]] = b[move[0]][:-1];
		returncode = 0;
		return returncode;

	if move[1] in ("S", "H", "C", "D"):
		if (srcCard - destCard) != 1:
			returncode = 3;
			return returncode;
		b[move[1]] = chr(srcCard);
		if move[0] in ("Q", "W", "E", "R"):
			b[move[0]] = "";
		elif move[0] in ("S", "H", "C", "D"):
			b[move[0]] = chr(srcCard - 1);
		else:
			b[move[0]] = b[move[0]][:-1];
		returncode = 0;
		return returncode;


	if (srcCardSuit & REDMASK) == (destCardSuit & REDMASK):
		returncode = 4;
		return returncode;

	if (destCardValu - srcCardValu) != 1:
		returncode = 5;
		return returncode;

	b[move[1]] = b[move[1]] + chr(srcCard);
	if move[0] in ("Q", "W", "E", "R"):
		b[move[0]] = "";
	elif move[0] in ("S", "H", "C", "D"):
		b[move[0]] = chr(srcCard - 1);
	else:
		b[move[0]] = b[move[0]][:-1];
	returncode = 0;
	return returncode;

def checkVictory(b: dict[str, str]) -> int:
	doneSuits = [ "L", "\\", "l", "|" ];
	if b["S"] in doneSuits and b["H"] in doneSuits and b["C"] in doneSuits and b["D"] in doneSuits:
		return 1;
	else:
		return 0;

def checkLoss(b: dict[str, str]) -> int:
	#any free cells								1
	#any free columns							2
	#do the bottom cards of any column fit in the home cells		3
	#do any of the cards in the free cells fit in the home cells		4

	#do any of the cards in the free cells fit under a column		5
	#do any of the bottom cards fit under any other bottom card		6
	if "" in b.values():
		return 0;
	if chr(ord(b["S"][-1]) + 1) in [ b["1"][-1], b["2"][-1], b["3"][-1], b["4"][-1], b["5"][-1], b["6"][-1], b["7"][-1], b["8"][-1] ]:
		return 0;
	if chr(ord(b["H"][-1]) + 1) in [ b["1"][-1], b["2"][-1], b["3"][-1], b["4"][-1], b["5"][-1], b["6"][-1], b["7"][-1], b["8"][-1] ]:
		return 0;
	if chr(ord(b["C"][-1]) + 1) in [ b["1"][-1], b["2"][-1], b["3"][-1], b["4"][-1], b["5"][-1], b["6"][-1], b["7"][-1], b["8"][-1] ]:
		return 0;
	if chr(ord(b["D"][-1]) + 1) in [ b["1"][-1], b["2"][-1], b["3"][-1], b["4"][-1], b["5"][-1], b["6"][-1], b["7"][-1], b["8"][-1] ]:
		return 0;
	if chr(ord(b["Q"][-1]) + 1) in [ b["1"][-1], b["2"][-1], b["3"][-1], b["4"][-1], b["5"][-1], b["6"][-1], b["7"][-1], b["8"][-1] ]:
		return 0;
	if chr(ord(b["W"][-1]) + 1) in [ b["1"][-1], b["2"][-1], b["3"][-1], b["4"][-1], b["5"][-1], b["6"][-1], b["7"][-1], b["8"][-1] ]:
		return 0;
	if chr(ord(b["E"][-1]) + 1) in [ b["1"][-1], b["2"][-1], b["3"][-1], b["4"][-1], b["5"][-1], b["6"][-1], b["7"][-1], b["8"][-1] ]:
		return 0;
	if chr(ord(b["R"][-1]) + 1) in [ b["1"][-1], b["2"][-1], b["3"][-1], b["4"][-1], b["5"][-1], b["6"][-1], b["7"][-1], b["8"][-1] ]:
		return 0;

	i = 1;
	pack = [];
	stack = [];
	while i < 9:
		pack.append(ord(b[str(i)][-1]));
		i += 1;
	for a in [ "Q", "W", "E", "R" ]:
		stack.append(ord(b[a][-1]));
	stackpack = pack + stack;
	for card in stackpack:
		for dard in pack:
			if ((card & REDMASK) != (dard & REDMASK)) and ((dard & VALUMASK) - (card & VALUMASK)) == 1:
				return 0;

	return 1;

def colorPrint(bs: str, b: dict[str,str], src: str="") -> str:
	validList = ["Q", "W", "E", "R", "S", "H", "C", "D", "1", "2", "3", "4", "5", "6", "7", "8"];
	newString = bs;
	redRegex = re.compile(r".(♥|♦)");
	goldRegex = re.compile(r"(\||\-|¦)");
	locList = [];
	newString = esc("30;42") + bs;
	for match in re.finditer(redRegex, newString):
		locList.append(match.span()[0]);
	i = 0;
	while i < len(locList):
		cursor = locList[i] + 16*i;
		newString = newString[:cursor] + esc("31;42") + newString[cursor:cursor + 2] + esc("30;42") + newString[cursor + 2:];
		i += 1;

	locList = [];
	for match in re.finditer(goldRegex, newString):
		locList.append(match.span()[0]);
	i = 0;
	while i < len(locList):
		cursor = locList[i] + 16*i;
		newString = newString[:cursor] + esc("37;43") + newString[cursor:cursor + 1] + esc("30;42") + newString[cursor + 1:];
		i += 1;
	if src != "" and src[0] in validList:
		if b != {}:
			if b[src[0]] != "":
				sel = newString.index(cardSymbol(ord(b[src[0]][-1])));
				newString = newString[:sel] + esc("35;42") + newString[sel:sel + 2] + esc("30;42") + newString[sel + 2:];
	newString = esc("37;40") + "Q    W    E    R    S    H    C    D\n" + newString + esc("37;40") + "1    2    3    4    5    6    7    8\n";
	print(newString);
	return newString;

def colorSolution(move: str) -> str:

	if move.isdigit():
		cm = esc("30;42") + move[0] + esc("30;43") + move[1] + esc("37;40") + " ";
	else:
		cm = cellColours[move[0].upper()] + move[0] + cellColours[move[1].upper()] + move[1] + esc("37;40") + " ";
	return cm;

def clearScreen():
	if os.name == 'nt':
		os.system("cls");
	else:
		os.system("clear");

##Base Game Loop
def main(pm: int=1):
	init();

	clearScreen();

	done = 0;
	cont = 1;
	solution = "";
	moves = 0;
	argstring = sys.argv[1] if len(sys.argv) > 1 else None;
	deck = makeDeck(argstring);
	if(argstring is None):
		deck = riffleShuffle(deck, shufflecount);
	shuffle = deckString(deck);
	board = dealBoard(deck);
	try:
		while cont:
			colorPrint(boardString(board), board);
			print(esc("37;40") + "Shuffle: " + shuffle);
			print(esc("37;40") + str(moves) + " moves:\t" + solution);
			if pm == 1:
				src = input("Source: ");
				if src.upper() == "NO":
					break;
				clearScreen();
				colorPrint(boardString(board), board, src);
				print(esc("37;40") + "Shuffle: " + shuffle);
				print(esc("37;40") + str(moves) + " moves:\t" + solution);
				print("Source: " + src);
				dest = input("Destination: ");
				if dest.upper() == "NO":
					break;
				if len(src) != 0 and len(dest) != 0:
					move = src[0] + dest[0];
				else:
					move = "00";
				if move.upper() == "NO":
					break;
			else:
				move = input("Move: ");
				if move.upper() == "NO":
					break;
				if len(move) < 2:
					move = "00";
			clearScreen();
			invalid = makeMove(move, board);
			if invalid:
				print("Invalid move. Please try again. (" + str(invalid) + ")");
			else:
				solution = solution + colorSolution(move);
				moves = moves + 1;
				done = checkVictory(board);
				cont -= checkLoss(board);
				cont -= done;

	except KeyboardInterrupt:
		cont = 0;
		clearScreen();
		print("Quit.");
		colorPrint(boardString(board), board);
		print(esc("37;40") + "Shuffle: " + shuffle);
		print(esc("37;40") + str(moves) + " moves:\t" + solution);
	if done:
		print("Congration you done it!");
		argstring = sys.argv[1] if len(sys.argv) > 1 else None;
		deck = makeDeck(argstring);
		if(argstring is None):
			deck = riffleShuffle(deck, shufflecount);
		shuffle = deckString(deck);
		board = dealBoard(deck);
		colorPrint(boardString(board), board);
		print(esc("37;40") + "Shuffle: " + shuffle);
		print(esc("37;40") + str(moves) + " moves:\t" + solution);

if __name__ == "__main__":
	main(2);