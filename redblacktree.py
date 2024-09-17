class Node:
    """
        This class creates a node with relevant data to be used in
        the following red-black tree class    
    """

    __author__ = "Silver Lippert"
    __version__ = "23.11.5"
    
    is_black = False
    key = None
    value = None
    size = 0

    left_child = None
    right_child = None

    def __init__(self, k, v, s = 0,  is_bl = False):
        self.is_black = is_bl
        self.key = k
        self.value = v
        self.size = s


class RedBlackTree:

    """
        This program implements a red-black tree data structure, along with
        some useful methods to analyze various aspects of the tree.    
    """

    __author__ = "Silver Lippert"
    __version__ = "23.11.5"

    root = None

    # inserts a new k / v pair. Assume neither is none
    def put(self, key, value):
        """
            This method takes a key / value pair and inserts it into the red-black tree.
            If the key already exists, it will replace the old value with the input one.
        """
        self.root = self.__find_and_add(self.root, key, value) # helper method
        self.root.is_black = True
        

    # get returns value of given key, or none if key does not exist
    def get(self, key):
        """
            This method takes a key and searches the tree for it. It will return
            the value associated with the key, or none if the key is not within the tree.
        """
        tree = []
        tree.append(self.root)

        for item in tree: # loop through the tree
            if item:
                if item.key == key:
                    return item.value
                elif item.key > key:
                    tree.append(item.left_child)
                else:
                    tree.append(item.right_child)
        return None


    # removed a k / v pair, returns deleted val, or none is key DNE
    def delete(self, key):
        """
            This method takes a key as input, and searches the tree for it. If found,
            it then removes that key / value pair from the tree.
        """
        val = self.get(key)
        if val and self.root: # if the key exists, and the root exists
            self.root.is_black = False # make root red
            self.root = self.__find_and_delete(self.root, key) # helper method
            if self.root:
                self.root.is_black = True
            return val
        else: # if key or root DNE
            return None

    # returns true if key is present
    def contains_key(self, key) -> bool:
        """
            This method takes a key as input, and returns a boolean
            indicating whether the key is in the tree.
        """
        if self.get(key):
            return True
        return False

    # returns true if value is present
    def contains_value(self, value) -> bool:
        """
            This method takes a value as input, and returns a boolean
            indicating whether the key is in the tree.
        """
        if self.reverse_lookup(value):
            return True
        return False

    # returns true if tree is empty
    def is_empty(self) -> bool:
        """
            This method returns a boolean indicating whether the tree has
            any nodes in it.
        """
        if self.root == None:
            return True
        return False

    # returns num of k / v pairs
    def __len__(self)-> int: 
        """
        returns number of key / value pairs
        """
        if self.root:
            return self.root.size
        return 0

    # finds key that maps to val, or none if DNE
    def reverse_lookup(self, value):
        """
           This method takes a value as input, and finds the key that maps to it.
           It returns the key, or none if the key DNE. 
        """
        tree = []
        tree.append(self.root)
        for item in tree: # loop through the tree
            if item:
                if item.value == value:
                    return item.key
                tree.append(item.left_child) # search both nodes
                tree.append(item.right_child)
        return None

    # returns smallest key, or none if there is none
    def find_first_key(self):
        """
            This method finds and returns the smallest key in order.
        """
        tree = []
        tree.append(self.root)
        for item in tree: # loop through the tree
            if item and item.left_child:
                tree.append(item.left_child)
        return tree.pop().key

    # returns largest key or none if there is none
    def find_last_key(self):
        """
            This method finds and returns the largest key in order.
        """
        tree = []
        tree.append(self.root)
        for item in tree: # loop through the tree
            if item and item.right_child:
                tree.append(item.right_child)
        return tree.pop().key

    # returns key at the root or none if not there
    def get_root_key(self):
        """
            This method returns the key that is situated at the root position.
        """
        if self.root:
            return self.root.key
        return None

    # returns predecessor of given key or none if key DNE or has no pred.
    def find_predecessor(self, key):
        """
            This method takes a key as input, and then finds and returns its predecessor.
            Returns None if the key DNE, or if it has no predecessor.
        """
        tree = []
        tree.append(self.root)
        found = None
        recent_right = None

        for item in tree: # find Node w/ input key
            if item:
                if item.key > key:
                    tree.append(item.left_child)
                elif item.key == key:
                    found = item
                    break
                else:
                    tree.append(item.right_child)
                    recent_right = item # remember node travelled left from

        
        if found == None: # if key is not found
            return None
        else:
            tree = []
            tree.append(found.left_child)
            for item in tree: # find the child furthest to the right, if exists
                if item and item.right_child:
                    tree.append(item.right_child)

        final_node = tree.pop()

        if final_node: # if a predecessor beneath the key exists
            return final_node.key
        elif recent_right: # if the most recent right node before the key exists
            return recent_right.key
        else:
            return None

    # returns successor of key, or none if key DNE or has no succ.
    def find_successor(self, key):
        """
            This method takes a key as input, and searches for and returns its
            successor. It may return None if the key DNE, or has no successor.
        """
        tree = []
        tree.append(self.root)
        found = None
        recent_left = None

        for item in tree: # find Node w/ input key
            if item:
                if item.key > key:
                    tree.append(item.left_child)
                    recent_left = item # remember node travelled left from
                elif item.key == key:
                    found = item
                    break
                else:
                    tree.append(item.right_child)
        
        if found == None: # if key DNE
            return None
        else:
            tree = []
            tree.append(found.right_child)
            for item in tree: # search for leftmost child
                if item and item.left_child:
                    tree.append(item.left_child)

        final_node = tree.pop()

        if final_node: # if decendant successor exists
            return final_node.key
        elif recent_left: # if ancestor successor exists
            return recent_left.key
        else:
            return None

    # returns rank of key, or -1 if key DNE
    def find_rank(self, key) -> int:
        """
            This method takes a key as input, and returns the rank
            that it is in the tree. It will return -1 if the key DNE.
        """
        tree = []
        tree.append(self.root)
        rank = 0

        for item in tree: # loop through the tree
            if item:
                if item.key > key:
                    tree.append(item.left_child)
                elif item.key == key:
                    if item.left_child:
                        rank -= -item.left_child.size
                    return rank
                else:
                    rank -= -1
                    if item.left_child:
                        rank -= -item.left_child.size
                    tree.append(item.right_child)


    # returns key of the given rank, or none if rank is invalid, 0 index
    def select (self, rank: int):
        """
            This method takes a rank as input, and returns the key it is
            associated with. It will return None if the rank is invalid.
            The ranks are 0 indexed.
        """
        tree = []
        tree.append(self.root)
        left_size = 0

        for item in tree: # loop through tree
            if item:
                if item.left_child:
                    left_size = item.left_child.size
                else: 
                    left_size = 0
                if left_size > rank:
                    tree.append(item.left_child)
                elif left_size == rank:
                    return item.key
                else:
                    rank = rank - 1 - item.left_child.size
                    tree.append(item.right_child)

    # returns num of red nodes in the tree
    def count_red_nodes(self)-> int:
        """
            This method counts and returns the number of red nodes
            in the tree.
        """
        tree = []
        num_red = 0
        tree.append(self.root)

        for item in tree: # loop through tree
            if item == None:
                continue
            else:
                tree.append(item.left_child)
                tree.append(item.right_child)
                if not item.is_black:
                    num_red -= -1

        return num_red

    # returns height of tree, where an empty tree has height of 0
    def calc_height(self) -> int:
        """
            This method returns the height of the longest path in the tree.
            An empty tree returns 0.
        """
        height = 1
        max_height = 0
        tree = []
        tree.append((self.root, height))

        for item in tree: # loop through the tree
            if item[0] == None:
                continue
            else:
                height = item[1]
                if height > max_height:
                    max_height = height
                tree.append((item[0].left_child, height + 1))
                tree.append((item[0].right_child, height + 1))
        return max_height


    # returns black height of tree, or 0 for empty tree
    def calc_black_height(self)-> int:
        """
            This method calculates and returns the black height of the tree.
            Returns 0 for an empty tree.
        """
        node = self.root
        height = 0
        while node != None: # go down the right side of the tree so there are no red nodes
            height -= -1
            node = node.right_child
        return height

    # returns av distance of nodes from the root. Empty trees return NaN
    def calc_average_depth(self) -> float:
        """
            This method calculates and returns the average height of each node 
            in the tree. Empty trees return NaN.
        """
        if self.is_empty():
            return float('nan')
        tree = []
        tree.append((self.root, 0))
        counter = 0
        total_height = 0

        for item in tree: # loop through the tree
            if item[0] == None:
                continue
            else:
                counter = item[1]
                total_height -= -counter
                tree.append((item[0].left_child, counter+1))
                tree.append((item[0].right_child, counter+1))
                
        return total_height / (self.root.size -1)
        
        

    # performs a color flip on input node and its children
    def __color_flip(self, parent)-> Node:
        parent.left_child.is_black  = parent.is_black
        parent.right_child.is_black  = parent.is_black
        parent.is_black = not parent.is_black
        return parent

    # performs a left rotation on input node
    def __left_rotate(self, parent)-> Node:
        t_key = parent.key
        t_val = parent.value
        temp = parent.right_child

        # parent and temp swap keys and values
        parent.key = temp.key
        parent.value = temp.value
        temp.key = t_key
        temp.value = t_val

        # rearrange children
        parent.right_child = temp.right_child
        temp.right_child = temp.left_child
        temp.left_child = parent.left_child
        parent.left_child = temp

        # adjust the size of each node
        self.__fix_size(temp)
        self.__fix_size(parent)
        return parent

    
    # performs a right rotation on input node
    def __right_rotate(self, parent: Node)-> Node:
        t_key = parent.key
        t_val = parent.value
        temp = parent.left_child

        # parent and temp swap keys and values
        parent.key = temp.key
        parent.value = temp.value
        temp.key = t_key
        temp.value = t_val

        # rearrange children
        parent.left_child = temp.left_child
        temp.left_child = temp.right_child
        temp.right_child = parent.right_child
        parent.right_child = temp

        # adjust the size of each node
        self.__fix_size(temp)
        self.__fix_size(parent)
        return parent
        

    def __find_and_delete(self, root, key) -> Node:

        # if node is a leaf
        if not root.left_child and not root.right_child:
            if root.key == key: # if node matches, delete
                return None
            else:
                return root # otherwise, do nothing
            
        elif not root.right_child and root.left_child: # if left only
            if root.key == key: # if match, promote left child
                return root.left_child
            else: # note: this child HAS to be red, so no changes are needed
                root.left_child = self.__find_and_delete(root.left_child, key) # otherwise, recurse

        elif root.left_child and root.right_child: # if left and right child

            # should only come up on rotation situations where right
            # child needed to be red in order to step into it
            if root.left_child.is_black and not root.right_child.is_black:
                if root.key < key:
                    root.right_child = self.__find_and_delete(root.right_child, key)
                elif root.key == key:
                    root = self.__swap_with_pred(root)
                else: # this shouldnt happen? but just in case...
                    root = self.__left_rotate(root)
                    root.left_child = self.__find_and_delete(root.left_child, key)

            elif root.left_child.is_black: # if both children are black   
                root = self.__color_flip(root) # make children red
                if root.key > key:
                    root.left_child = self.__find_and_delete(root.left_child, key)
                elif root.key < key:
                    root.right_child = self.__find_and_delete(root.right_child, key)
                else: # current node needs to be deleted
                    root = self.__swap_with_pred(root) # this is now its pred

            elif not root.left_child.is_black: # if left is red
                if root.key > key: # no changes needed
                    root.left_child = self.__find_and_delete(root.left_child, key)
                elif root.key < key:
                    root = self.__right_rotate(root) # changes root to the l child
                    # this will basically call it on the same node, but in a different position
                    root.right_child = self.__find_and_delete(root.right_child, key)
                else: # found the key we need
                    root = self.__swap_with_pred(root)

        # on the way back up...

        # if left DNE but right exists
        if not root.left_child and root.right_child:
            root = self.__left_rotate(root)

        # if r and l children are both red
        if root.is_black and root.left_child and not root.left_child.is_black and root.right_child and not root.right_child.is_black:
            root = self.__color_flip(root)

        # if right child is red and root is black
        if root.left_child and root.left_child.is_black and root.right_child and not root.right_child.is_black:
            root = self.__left_rotate(root)

        # if r child is red and its r child is red
        if root.right_child and not root.right_child.is_black and root.right_child.right_child and not root.right_child.right_child.is_black:
            root = self.__left_rotate(root)

        # if l child is red and its r child is red
        if root.left_child and not root.left_child.is_black and root.left_child.right_child and not root.left_child.right_child.is_black:
            root.left_child = self.__left_rotate(root.left_child)

        # if l child is red and its l child is red
        if root.left_child and not root.left_child.is_black and root.left_child.left_child and not root.left_child.left_child.is_black: 
                root = self.__right_rotate(root)

        # if both children are red again due to rotation
        if root.is_black and root.left_child and not root.left_child.is_black and root.right_child and not root.right_child.is_black:
            root = self.__color_flip(root)

        self.__fix_size(root)
        return root


    def __swap_with_pred(self, root) -> Node:
        # replace key with pred key
        # get val associated with key
        # call delete on pred
        pred_key = self.find_predecessor(root.key)
        pred_value = self.get(pred_key)

        root.key = pred_key
        root.value = pred_value

        root.left_child = self.__find_and_delete(root.left_child, pred_key) # delete pred to promote it
        
        return root


    # adding to tree function, recursive, returns Node
    def __find_and_add(self, root, key, value) -> Node:
        # finding / modifying / adding Node with key
        
        if root == None:
            return Node(key, value, 1)
        if root.key == key:
            root.value = value
            return root
        elif root.key < key:
            root.right_child = self.__find_and_add(root.right_child, key, value)
        else:
            root.left_child = self.__find_and_add(root.left_child, key, value)


        # fixing the tree now that its all messed up
        if root.right_child and not root.right_child.is_black:
            self.__left_rotate(root)

        if root.left_child and root.left_child.left_child and not root.left_child.is_black and not root.left_child.left_child.is_black:
            self.__right_rotate(root)


        if root.left_child and root.right_child and not root.left_child.is_black and not root.right_child.is_black:
            self.__color_flip(root)

        self.__fix_size(root)

        return root

    # quick method for recalculating size field
    def __fix_size(self, root):
        root.size = 1
        if root.left_child:
            root.size -= -root.left_child.size
        if root.right_child:
            root.size -= -root.right_child.size


    # method to print out the tree for testing
    def string(self, root = None, height = 0):
        if height == 0:
            root = self.root
        if root == None:
            return ""
        tab = "\t" * height
        return (f'{tab}{root.is_black}, ({root.key}, {root.value})\n L{self.string(root.left_child, height+1)}\n R{self.string(root.right_child, height+1)}')
    