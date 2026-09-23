import unittest
from structures import Stack, Queue


class TestStack(unittest.TestCase):
    def setUp(self):
        self.stack = Stack()

    def test_push_and_pop(self):
        self.stack.push(1)
        self.stack.push(2)
        self.assertEqual(self.stack.pop(), 2)
        self.assertEqual(self.stack.pop(), 1)
        self.assertTrue(self.stack.is_empty())

    def test_peek(self):
        self.stack.push("A")
        self.assertEqual(self.stack.peek(), "A")
        self.assertEqual(self.stack.size(), 1)

    def test_empty_pop_raises_error(self):
        with self.assertRaises(IndexError):
            self.stack.pop()


class TestQueue(unittest.TestCase):
    def setUp(self):
        self.queue = Queue()

    def test_enqueue_and_dequeue(self):
        self.queue.enqueue(10)
        self.queue.enqueue(20)
        self.assertEqual(self.queue.dequeue(), 10)
        self.assertEqual(self.queue.dequeue(), 20)
        self.assertTrue(self.queue.is_empty())

    def test_peek(self):
        self.queue.enqueue("First")
        self.assertEqual(self.queue.peek(), "First")
        self.assertEqual(self.queue.size(), 1)

    def test_empty_dequeue_raises_error(self):
        with self.assertRaises(IndexError):
            self.queue.dequeue()


if __name__ == '__main__':
    unittest.main()