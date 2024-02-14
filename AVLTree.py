"""A class representing a node in an AVL tree"""


class AVLNode(object):
	"""Constructor, you are allowed to add more fields.

	@type key: int or None
	@param key: key of your node
	@type value: any
	@param value: data of your node
	@type parent: node
	@param parent: parent of self
	"""
	def __init__(self, key=None, value=None, parent=None):
		self.key, self.value, self.parent = key, value, parent
		if key is None:  # node is virtual
			self.left = None
			self.right = None
			self.height = -1
			self.size = 0

		else:  # node is leaf
			self.left = AVLNode(None, None, self)
			self.right = AVLNode(None, None, self)
			self.height = 0
			self.size = 1

	"""returns the key
	
	@rtype: int or None
	@returns: the key of self, None if the node is virtual
	"""
	def get_key(self):
		return self.key

	"""returns the value
	
	@rtype: any
	@returns: the value of self, None if the node is virtual
	"""
	def get_value(self):
		return self.value

	"""returns the left child
	
	@rtype: AVLNode
	@returns: the left child of self, None if there is no left child (if self is virtual)
	"""
	def get_left(self):
		return self.left

	"""returns the right child

	@rtype: AVLNode
	@returns: the right child of self, None if there is no right child (if self is virtual)
	"""
	def get_right(self):
		return self.right

	"""returns the parent 

	@rtype: AVLNode
	@returns: the parent of self, None if there is no parent
	"""
	def get_parent(self):
		return self.parent

	"""returns the height

	@rtype: int
	@returns: the height of self, -1 if the node is virtual
	"""
	def get_height(self):
		return self.height

	"""returns the size of the subtree

	@rtype: int
	@returns: the size of the subtree of self, 0 if the node is virtual
	"""
	def get_size(self):
		return self.size

	"""sets key

	@type key: int or None
	@param key: key
	"""
	def set_key(self, key):
		self.key = key
		return None

	"""sets value

	@type value: any
	@param value: data
	"""
	def set_value(self, value):
		self.value = value
		return None

	"""sets left child

	@type node: AVLNode
	@param node: a node
	"""
	def set_left(self, node):
		self.left = node
		return None

	"""sets right child

	@type node: AVLNode
	@param node: a node
	"""
	def set_right(self, node):
		self.right = node
		return None

	"""sets virtual node as son
	
	@pre: self.is_real_node
	@pre: if left is None, self.parent is not None
	if (@param left == True) => sets as left child of node 
	if (@param left == False) => sets as right child of node
	if (@param left is None) => sets to replace node as node.parent's son  
	"""

	def virtual_son(self, left=None):
		if left is None:
			par = self.get_parent()
			if par is None:  # self is root
				return True  # flags that tree's node needs to be None
			left = (par.get_left() == self)  # checks if self is left or right son
		else:
			par = self
		if left:
			par.set_left(AVLNode(None, None, par))
		else:
			par.set_right(AVLNode(None, None, par))
		return None

	"""sets parent

	@type node: AVLNode
	@param node: a node
	"""
	def set_parent(self, par, detach=False):
		if detach and self.parent is not None:
			self.virtual_son()
		self.parent = par  # replace node's parent to be par
		if par is None:
			return True  # flags that the node is now some tree's root
		if self.get_key() > par.get_key():
			par.set_right(self)
		else:
			par.set_left(self)
		return False

	"""sets the height of the node

	@type h: int
	@param h: the height
	"""
	def set_height(self, h):
		self.height = h
		return None

	"""sets the size of node

	@type s: int
	@param s: the size
	"""
	def set_size(self, s):
		self.size = s
		return None

	"""increases node's size by n
	to reduce size use negative n"""
	def add_to_size(self, n):
		self.size += n
		return None

	"""updates the node's size&height to the correct
	one according to his current sub-tree
	@returns: True if node's height hasn't changed, else False"""
	def update_node(self, size=True, height=True):
		if size:
			self.set_size(1 + self.get_left().get_size() + self.get_right().get_size())
		if height:
			curr = self.height
			self.set_height(1 + max(self.get_left().get_height(), self.get_right().get_height()))
			if self.height != curr:
				return True
		return False

	"""returns whether self is not a virtual node 

	@rtype: bool
	@returns: False if self is a virtual node, True otherwise.
	"""
	def is_real_node(self):
		return self.height != -1

	"""computes node's BF"""
	def getBF(self):
		return self.get_left().get_height() - self.get_right().get_height()

	"""returns the node's successor in the Tree"""
	def get_successor(self):
		if not self.get_right().is_real_node():
			x = self
			y = self.get_parent()
			while y is not None and x == y.get_right():
				x = y
				y = x.get_parent()
			return y
		return self.get_right().go_to_h(-1, True)  # finds sub-tree's minimum

	"""
	* * * for FT-insert * * *
	returns the node's predecessor in the tree
	"""
	def get_predecessor(self):
		x = self
		if x.get_left().is_real_node():  # node has left son
			x = x.get_left()
			return x.go_to_h(-1, False)  # return max of node's left tree
		if x.get_parent() is not None:  # node's left tree is empty
			return x.get_parent()
		return None  # node is the only node in the tree

	"""finds a node with height h in the node's leftmost or rightmost subtree, or minimal if h == -1
	@type h: int
	@param h: height to search
	@type left: bool
	@param left: if True -> travels through the left subtree, if False -> travels through right
	@rtype: AVLNode
	"""
	def go_to_h(self, h, left: bool):
		x = self
		if left:
			while x.get_left().is_real_node() and x.get_height() > h:
				x = x.get_left()
		else:  # same but inverted
			while x.get_right().is_real_node() and x.get_height() > h:
				x = x.get_right()
		return x


"""
A class implementing an AVL tree.
"""


class AVLTree(object):

	"""
	Constructor, you are allowed to add more fields.

	"""
	def __init__(self, node=None):
		self.root = node
		self.Tmin = node
		# self.Tmax = node   #for FT-insert

	"""changes tree's root to be @param new_root"""
	def set_root(self, new_root):
		if self.root is None or new_root is None:
			# self.Tmax = new_root   #for FT-insert
			self.Tmin = new_root
		self.root = new_root

	"""returns the root of the tree representing the dictionary

	@rtype: AVLNode
	@returns: the root, None if the dictionary is empty
	"""
	def get_root(self):
		return self.root

	"""sets the tree's minimum """
	def set_min(self, node):
		self.Tmin = node

	"""returns the tree's minimum"""
	def get_min(self):
		return self.Tmin

	"""
	* * * for FT-insert * * *
	sets the tree's maximum
	"""
	# def set_max(self, node):
	# 	self.Tmax = node

	"""
	* * * for FT-insert * * *
	sets the tree's minimum"""
	# def get_max(self):
	# 	return self.Tmax

	"""updates self's Tmin&Tmax according to the node inserted/deleted
	fit for insertion if insert == True, for deletion if insert == False
	@pre: for insert&delete - node is AVLNode, not None
	fir for re-generated tree (split, join..) by default (insert&node == None)"""
	def update_min(self, node=None, insert=None):
		if insert:
			if self.get_min() is None:
				self.set_min(node)
			# if self.get_max() is None:    #for FT-insert
				# self.set_max(node)    #for FT-insert

			if node.get_key() < self.get_min().get_key():
				self.set_min(node)
			# if node.get_key() > self.get_max().get_key():   #for FT-insert
				# self.set_max(node)   #for FT-insert

		elif insert == False:
			if self.get_min() == node:
				self.set_min(node.get_successor())
			# if self.get_max() == node:   #for FT-insert
				# self.set_max(node.get_predecessor())   #for FT-insert

		elif self.get_root() is None:
			self.set_min(None)
			# self.set_max(None)   #for FT-insert

		else:
			self.set_min(self.get_root().go_to_h(-1, True))
			# self.set_max(self.get_root().go_to_h(-1, False))  #for FT-insert

		return self

	"""returns the number of items in dictionary 

	@rtype: int
	@returns: the number of items in dictionary 
	"""
	def size(self):
		if self.get_root() is None:
			return 0
		return self.root.get_size()

	"""returns tree's height"""
	def tree_height(self):
		if self.get_root() is None:
			return -1
		return self.root.get_height()

	"""searches for a node in the dictionary corresponding to the key

	@type key: int
	@param key: a key to be searched
	@rtype: AVLNode
	@returns: node corresponding to key.
	"""
	def search(self, key):
		x = self.search_closest(key)
		if x is None:
			return None  # tree is empty
		return x if x.get_key() == key else None

	"""searches for a node in the dictionary corresponding to the key, or the closest node
	
	@type key: int
	@param key: a key to be searched
	@rtype: AVLNode
	@returns: node corresponding to key
	"""

	def search_closest(self, key):
		if self.get_root() is None:  # empty tree
			return None
		x = self.root
		while x.is_real_node():
			if key == x.get_key():
				return x
			elif key < x.get_key():
				x = x.get_left()
			else:
				x = x.get_right()
		return x.get_parent()

	"""inserts val at position i in the dictionary

	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
	@type val: any
	@param val: the value of the item
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""
	def insert(self, key, val):
		y = AVLNode(key, val)
		if self.get_root() is None:
			self.set_root(y)
			self.set_min(y)
			return 0
		x = self.search_closest(key)
		y.set_parent(x)
		self.update_min(y, True)
		return self.fix_after(x)

	"""
	* * * * * * * * * * * * * * * * * * * * * * * * * * * 
	* * * * * * * * finger-Tree insertion * * * * * * * *
	* * * * un# relevant lines/methods before use * * * *
	* * * can be found by searching 'for FT-insert' * * *
	* * * * * * * * * * * * * * * * * * * * * * * * * * *
	
	performs insert using finger-tree technic:
	starting from tree's max node and going up to the first
	node ('x') with key smaller then inserted-key ->
	then performing normal insert, only on the node's sub-tree   
	"""
	def FT_insert(self, key, val):
		y = AVLNode(key, val)
		if self.get_root() is None:
			self.set_root(y)
			self.set_min(y)
			return 0
		# up till here - same as normal insert
		x = self.get_max()
		cnt = 0
		while x.get_key() > key and x.get_parent() is not None:
			x = x.get_parent()
			cnt += 1
		sub_tree = AVLTree(x)
		# from here on - same as normal insert (only now in a smaller tree)
		par, add = sub_tree.search_closest(key)
		# for tests - change search_closest to counter that returns (node, cnt)
		y.set_parent(par)
		self.update_min(y, True)
		cnt += self.fix_after(par)
		return self.size()-self.rank(y), cnt  # num of changes, cnt

	"""deletes node from the dictionary

	@type node: AVLNode
	@pre: node is a real pointer to a node in self
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""
	def delete(self, node: AVLNode):
		cnt = 0
		self.update_min(node, False)
		par = node.get_parent()
		sons = (node.get_left(), node.get_right())
		if sons[0].is_real_node() and sons[1].is_real_node():  # node has 2 real sons
			suc = node.get_successor()
			h = node.get_height()
			par = self.full_delete(sons[0], sons[1], par, suc)
			if h != suc.get_height():
				cnt += 1
		else:  # no has 1 son or no sons
			self.simple_delete(node, sons, par)
		return cnt + self.fix_after(par, None)

	"""basic (BST) deletion of a node less then 2 sons"""

	def simple_delete(self, node: AVLNode, sons, par):
		if sons[0].is_real_node():  # only left son
			if sons[0].set_parent(par):  # node is root - sons[0] needs to be new root
				self.set_root(sons[0])
		elif sons[1].is_real_node():  # only right son
			if sons[1].set_parent(par):  # node is root - sons[1] needs to be new root
				self.set_root(sons[1])
		else:  # node is leaf
			if node.virtual_son():  # check id node is root
				self.set_root(None)
		return None

	"""basic (BST) deletion of a node with 2 sons"""
	def full_delete(self, ls: AVLNode, rs: AVLNode, par, suc: AVLNode):
		suc_par = suc.get_parent()
		if suc.get_right().is_real_node():
			if suc != rs:
				suc.get_right().set_parent(suc_par)
		else:
			suc.virtual_son()

		if suc.set_parent(par):
			self.set_root(suc)

		if suc == rs:  # node's successor is his son, no change in suc.right
			suc.add_to_size(ls.get_size())
			suc.set_height(max(suc.get_height(), ls.get_height()+1))  # otherwise we might add an extra 1 to h
			ls.set_parent(suc)
			return ls
		else:
			rs.set_parent(suc)
			suc.set_size(ls.get_size() + rs.get_size() + 1)
			suc.set_height(1 + max(ls.get_height(), rs.get_height()))
		ls.set_parent(suc)

		return suc_par

	"""fixing after deletion/insertion
	counts the number of steps"""
	def fix_after(self, y: AVLNode, insert=True):
		total = self.update(y, insert)
		cnt_h = 0
		while y is not None:
			par = y.get_parent()
			if abs(y.getBF()) == 2:
				if insert:
					return cnt_h + self.rotation(y)  # stop after first rotation
				h_diff = par.get_height() if par is not None else 0
				total += self.rotation(y)
				if par is not None:
					h_diff -= par.get_height()  # might be missed count of height change
				total += abs(h_diff)
			else:
				cnt_h += 1
			if insert and cnt_h == total:   # stop if height hasn't changed
				break
			y = par
		return total

	"""returns an array representing dictionary 

	@rtype: list
	@returns: a sorted list according to key of tuples (key, value) representing the data structure
	"""
	def avl_to_array(self):
		lst = list()
		if self.get_root() is None:
			return lst

		def in_order(x: AVLNode):
			if x.is_real_node():
				in_order(x.get_left())
				lst.append((x.get_key(), x.get_value()))
				in_order(x.get_right())
			return lst

		return in_order(self.root)

	"""splits the dictionary at a given node

	@type node: AVLNode
	@pre: node is in self
	@param node: The intended node in the dictionary according to whom we split
	@rtype: list
	@returns: a list [left, right], where left is an AVLTree representing the keys in the 
	dictionary smaller than node.key, right is an AVLTree representing the keys in the 
	dictionary larger than node.key.
	"""

	def split(self, node: AVLNode):
		allJoins = []
		par = node.get_parent()
		if par is None:
			self.set_root(None)
			return [AVLTree(self.detach(node, True)).update_min(),
					AVLTree(self.detach(node, False)).update_min()]

		r_son = (par.get_right() == node)
		left = AVLTree(self.detach(node, True))
		right = AVLTree(self.detach(node, False))

		while par is not None:
			tmpP = par.get_parent()
			tmpS = (tmpP.get_right() == par) if tmpP is not None else None

			if r_son:
				L = AVLTree()
				L.set_root(self.detach(par, True))
				if left.get_root() is None:
					allJoins.append(AVLTree.join_by_node(left, L, par))
				else:
					allJoins.append(AVLTree.join_by_node(L, left, par))
			else:
				R = AVLTree()
				R.set_root(self.detach(par, False))
				if R.get_root() is not None:
					allJoins.append(AVLTree.join_by_node(right, R, par))
				else:
					allJoins.append(AVLTree.join_by_node(R, right, par))
			par = tmpP
			r_son = tmpS

		right.update_min()
		left.update_min()

		self.set_root(None)
		return [left, right]

	"""returns subtree of node as AVLTree
	and detach node from tree"""

	def detach(self, node: AVLNode, left=True):
		new_root = node.get_left() if left else node.get_right()
		node.set_parent(None, True)
		if not new_root.is_real_node():  # node's son is virtual (detaching 1 node tree)
			return None
		new_root.set_parent(None, True)
		node.update_node()
		return new_root

	"""joins self with key and another AVLTree

	@type tree: AVLTree 
	@param tree: a dictionary to be joined with self
	@type key: int 
	@param key: The key separating self with tree
	@type val: any 
	@param val: The value attached to key
	@pre: all keys in self are smaller than key and all keys in tree are larger than key,
	or the other way around.
	@rtype: int
	@returns: the absolute value of the difference between the height of the AVL trees joined
	"""
	def join(self, tree, key, val):
		x = AVLNode(key, val, None)
		if self.get_root() is not None and\
				(tree.get_root() is None or tree.get_root().get_key() < key):
			# only tree is empty or tree is the smaller-key's tree
			h_diff = tree.join_by_node(self, x)
		else:
			# self is empty or the smaller-key's tree
			h_diff = self.join_by_node(tree, x)

		self.update_min(self.get_root())
		tree.set_min(self.get_min())
		# tree.set_max(self.get_max())   #for FT-insert
		return h_diff

	"""joins self with another AVLTree by a given node
	@pre: if self is not empty - self.root.key < x.key < tree.root.key (tree also not empty)"""
	def join_by_node(self, tree, x: AVLNode):
		h1 = self.tree_height()  # self is always the smaller-keys tree or empty
		h2 = tree.tree_height()
		if self.get_root() is None:  # if self is empty
			if tree.get_root() is not None:  # tree is not empty
				y = tree.search_closest(x.get_key())
				x.set_parent(y)
				x.update_node()
				tree.fix_after(y)
				self.set_root(tree.get_root())
				return h2 + 1
			else:
				self.set_root(x)
				tree.set_root(x)
				x.update_node()
			return 1

		if h1 > h2:
			tree.connect(self, x, h2, False)
		else:  # h1 < h2
			self.connect(tree, x, h1, True)

		x.get_left().update_node() if x.get_left().is_real_node() else None
		x.get_right().update_node() if x.get_right().is_real_node() else None
		self.fix_after(x, None)
		tree.set_root(self.get_root())
		return abs(h1-h2)+1

	""" @pre: self.height <= tree.height
	prevent code duplicate...
	connects the nodes & sets new roots according to join's case"""
	def connect(self, tree, x, h, left_join=True):
		y = tree.get_root().go_to_h(h, left_join)
		par = y.get_parent()
		y.set_parent(x, True)
		self.get_root().set_parent(x)
		if par is not None:
			x.set_parent(par)
			self.set_root(tree.get_root())
		else:  # trees are at same height
			self.set_root(x)
			tree.set_root(x)
		x.update_node()
		self.get_root().update_node()

	"""compute the rank of node in the self

	@type node: AVLNode
	@pre: node is in self
	@param node: a node in the dictionary which we want to compute its rank
	@rtype: int
	@returns: the rank of node in self
	"""
	def rank(self, node: AVLNode):
		r = node.get_left().get_size()+1
		x = node
		par = x.get_parent()
		while x is not None and par is not None:
			if x == par.get_right():  # x is a right son
				r = r + par.get_left().get_size() + 1
			x = par
			par = par.get_parent()
		return r

	"""finds the i'th smallest item (according to keys) in self

	@type i: int
	@pre: 1 <= i <= self.size()
	@param i: the rank to be selected in self
	@rtype: int
	@returns: the item of rank i in self
	"""
	def select(self, i):

		def select_rec(node: AVLNode, j):
			r = node.get_left().get_size()+1 if node.is_real_node() else 0
			if j == r:
				return node
			elif j < r:
				return select_rec(node.get_left(), j)
				# search for the j'th smallest item in the left subtree
			else:
				return select_rec(node.get_right(), j - r)
				# search for the j-r'th smallest item in the right subtree

		if self.get_root().get_left().size+1 <= i:  # the wanted node is on tree's right side
			return select_rec(self.get_root(), i)  # can't use finger tree's
		# else - node's rank is smaller than root's rank.
		# find the minimal subtree that contain ranks {1,..i}
		x = self.get_min()
		while x.get_size() < i:
			x = x.get_parent()  # find the minimal node  tree
		return select_rec(x, i)   # preform select(i) on the minimal tree

	"""infers & performs the needed rotation at the node's level
	@pre: |BF(node)| == 2
	"""
	def rotation(self, node: AVLNode):
		cnt = 1
		par = node.get_parent()
		if node.getBF() == 2:
			l_son = node.get_left()
			if l_son.getBF() == -1:
				cnt += 1
				self.simple_rotate(l_son, True)
			self.simple_rotate(node, False)
		else:
			r_son = node.get_right()
			if r_son.getBF() == 1:
				cnt += 1
				self.simple_rotate(r_son, False)
			self.simple_rotate(node, True)

		self.update(par)
		return cnt

	"""does a rotation to the left (left == True) or to the right (left == False)"""
	# set_parent() also define node as the parent's son
	def simple_rotate(self, b: AVLNode, left: bool):
		a = b.get_right() if left else b.get_left()
		par = b.get_parent()
		if left:
			if a.get_left().is_real_node():
				a.get_left().set_parent(b)
			else:
				b.virtual_son(False)
		elif a.get_right().is_real_node():
			a.get_right().set_parent(b)
		else:
			b.virtual_son(True)
		b.set_parent(a)
		if a.set_parent(par):
			self.set_root(a)

		b.update_node()
		a.update_node()
		return None

	"""updates the tree nodes after operations
	fit for insertion if operation == True, for deletion if operation == False
	use the function on the soon-to-be-deleted or just-inserted node!
	fit for general cases (only height update) if operation=None
	"""

	def update(self, node: AVLNode, operation=None):
		cnt = 0
		if node is None:  # if deleted-node was root/empty tree was sent
			if self.get_root() is None: return 0
			return 1 if self.get_root().update_node() else 0
		x = node
		up_size = True if operation is None else False
		while x is not None:
			if not up_size:
				i = 1 if operation else -1
				x.set_size(x.get_size() + i)
			if x.update_node(up_size, True):
				cnt += 1  # node's height changed
			x = x.get_parent()
		return cnt
