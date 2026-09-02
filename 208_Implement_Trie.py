class TrieNode:
    def __init__(self, is_end=False):
        self.children = {str: TrieNode}
        self.is_end = is_end

class Trie:

    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        curr = self.root
        for c in word:
            if c not in curr.children:
                # insert the char
                curr.children[c] = TrieNode()
            curr = curr.children[c]
        curr.is_end = True

    def search(self, word: str) -> bool:
        curr = self.root
        for c in word:
            if c in curr.children:
                curr = curr.children[c]
            else:
                return False
        return curr.is_end

    def startsWith(self, prefix: str) -> bool:
        curr = self.root
        for c in prefix:
            if c in curr.children:
                curr = curr.children[c]
            else:
                return False
        return True     


# Your Trie object will be instantiated and called as such:
# obj = Trie()
# obj.insert("apple")
# param_2 = obj.search("apple")
# param_3 = obj.startsWith("app")