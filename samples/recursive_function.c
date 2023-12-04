int foo(int a) {
	if (a == 5) {
		return a;
	} else {
		a++;
		return foo(a);
	}
}

int main() {
	int x = foo(0);
	return x;
}
