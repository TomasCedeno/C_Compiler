int main() {
	int a = 2;

	if (a % 2 == 0) {
		goto even;
	} else {
		goto odd;
	}

	return 0;

even:
	return 1;

odd:
	return 2;
}
