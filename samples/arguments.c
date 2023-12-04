int sum(int a, int b) {
	return a + b;
}

int main() {
    int i = sum(4, 2);
    i = sum(2, 4);
    i = 2;
    sum(5, i);
    i = sum(1, 2) + sum(3, 4);
    return i;
}
