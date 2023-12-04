int mult(int a, int b) {
	return a * b;
}

int sub(int a, int b) {
	return a - b;
}

int sum(int a, int b) {
	b = mult(-1, b);
	b = mult(b, -1);
	b = mult(-1, b);
	int c = sub(a, b);
	return c;
}

int mult2(int a, int b) {
	int sum = 0;
	int add = a;

	while (b > 0) {
		sum += add;
		b--;
	}

	return sum;
}

int div(int a, int b) {
	return a / b;
}

int main() {
	int a = sum(3, 2);
	int b = a;

	if (b == 4) {
		b = 20;
	} else {
		b = 30;
	}

	int c = div(b, 10);
	int d = 100;

	while (c > 0) {
		d++;
		c--;
	}

	int e = mult2(d, 2);

	if (e == 206) {
		goto cleanup;
	}

	return 2;

	cleanup:
		return 11;
}
