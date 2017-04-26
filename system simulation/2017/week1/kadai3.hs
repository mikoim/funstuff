{-#LANGUAGE GADTs #-}

bs :: a ~ Double => (a -> a) -> a -> a -> a -> a
bs f a b ac
    | ac > abs  (a - b) = c
    | f c < 0 = bs f a c ac
    | f c > 0 = bs f c b ac
    | otherwise = c
    where c = (a + b) / 2

f1 x = sin x + x - 1
f2 x = x ** 3 - 8 * x ** 2 + 6 * x
f3 x = log x  - x ** 2 + 3
f4 x = sin x + 0.1 * x - 1

main = do
    -- sin(x) + x - 1
    print $ bs f1 (5.0) (-5.0) (0.0001)
    -- x^3 - 8 * x ^ 2 + 6 * x
    print $ bs f2 (5.0) (-5.0) (0.0001)
    -- log(x) - x ^ 2 + 3
    print $ bs f3 (5.0) (-5.0) (0.0001)
    -- sin(x) + 0.1 * x - 1
    print $ bs f4 (5.0) (-5.0) (0.0001)
