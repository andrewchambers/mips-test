void *volatile p;

int
main (void)
{
  int n = 0;
lab:;
    {
      int x[n % 1000 + 1];
      x[0] = 1;
      x[n % 1000] = 2;
      p = x;
      n++;
    }

    {
      int x[n % 1000 + 1];
      x[0] = 1;
      x[n % 1000] = 2;
      p = x;
      n++;
    }

  if (n < 100)
    goto lab;

  return 0;
}
