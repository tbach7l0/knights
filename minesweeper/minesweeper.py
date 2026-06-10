import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=16, width=16, mines=16):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        if self.count==len(self.cells):
            return self.cells

    def known_safes(self):
        if self.count==0:
            return self.cells 

    def mark_mine(self, cell):
        if cell in self.cells:
            self.cells.remove(cell)
            self.count-=1

    def mark_safe(self, cell):
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=16, width=16):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)
    def neighbors_position(self,cell): # return list of positions of given cell
        ans=[]
        i,j =cell
        h=self.height
        w=self.width
        if i==0:
            if j==0:
                ans=[(i+1,j),(i,j+1),(i+1,j+1)]
            elif j==w-1:
                ans=[(i,j-1),(i+1,j),(i+1,j-1)]
            else:
                ans=[(i,j-1),(i,j+1),(i+1,j),(i+1,j+1),(i+1,j-1)]
        elif i==h-1:
            if j==0:
                ans=[(i,j+1),(i-1,j+1),(i+1,j)]
            elif j==w-1:
                ans=[(i,j-1),(i-1,j),(i-1,j-1)]
            else:
                ans=[(i,j-1),(i,j+1),(i-1,j),(i-1,j+1),(i-1,j-1)]
        elif j==0:
            ans=[(i+1,j),(i-1,j),(i,j+1),(i+1,j+1),(i-1,j+1)]
        elif j==w-1:
            ans=[(i+1,j),(i-1,j),(i,j-1),(i+1,j-1),(i-1,j-1)]
        else:
            ans=[(i,j-1),(i,j+1),(i-1,j),(i+1,j),(i-1,j-1),(i-1,j+1),(i+1,j-1),(i+1,j+1)]
        return ans
    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) 
            5) 
        """
        #1
        self.moves_made.add(cell)
        #2
        self.mark_safe(cell)
        #3 
        neighbors_position_list=self.neighbors_position(cell)
        neighbors_position_set=set()
        c=count
        for i,j in neighbors_position_list:
            if (i,j) in self.mines:
                c-=1
                continue
            elif (i,j) in self.safes:
                continue
            else:
                neighbors_position_set.add((i,j))
        self.knowledge.append(Sentence(neighbors_position_set,c))


        #4: mark any additional cells as safe or as mines
            #if it can be concluded based on the AI's knowledge base
        for sentence in self.knowledge:
            if sentence.count==0:
                for c in set(sentence.cells):
                    self.mark_safe(c)
            elif sentence.count==len(sentence.cells):
                for c in set(sentence.cells):
                    self.mark_mine(c)


                    
        #5  add any new sentences to the AI's knowledge base
               #if they can be inferred from existing knowledge
        cur=[]
        n=len(self.knowledge)
        for i in range(n):
            for j in range(n):
                if self.knowledge[i].cells < self.knowledge[j].cells:
                    cur.append(Sentence(self.knowledge[j].cells-self.knowledge[i].cells,self.knowledge[j].count-self.knowledge[i].count))
                if self.knowledge[j].cells < self.knowledge[i].cells:
                    cur.append(Sentence(self.knowledge[i].cells-self.knowledge[j].cells,self.knowledge[i].count-self.knowledge[j].count))         
        for s in cur:
            if s not in self.knowledge:
                self.knowledge.append(s)
                print(s)
        print(self.safes)


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for i in range(self.height):
            for j in range(self.width):
                if (i,j) not in self.moves_made and (i,j) in self.safes:
                    return (i,j)

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        for i in range(self.height):
            for j in range(self.width):
                if (i,j) not in self.moves_made and (i,j) not in self.mines:
                    return (i,j)
