square :: Int -> Int
square x = x * x

test :: Int -> Bool
test x = (x > 100)

suma_patrate :: [Int] -> Int
suma_patrate lista = foldr (+) 0 (map square (filter odd lista))

all_true :: [Bool] -> Bool
all_true lista = foldr (&&) True lista

any_true :: [Bool] -> Bool
any_true lista = foldr (||) True lista

allVerifies :: (Int -> Bool) -> [Int] -> Bool
allVerifies func lista = all_true (map func lista)

anyVerifies :: (Int -> Bool) -> [Int] -> Bool
anyVerifies func lista = any_true (map func lista)

mapFoldr :: (Int -> Int) -> [Int] -> [Int]
mapFoldr func lista = foldr ()

main :: IO()
main = do
  print(anyVerifies test [1, 2, 3, 4, 101, 6])
