import Data.List

double :: Integer ->Integer
double x = x+x

maxim :: Int -> Int -> Int
maxim x y = if (x > y) then x else y

-- Functie suma patrate
func1 :: Int -> Int -> Int
func1 a b = a * a + b * b

-- Functie par/impar
func2 :: Int -> String
func2 a = if (a `mod` 2 == 0) then "par" else "impar"

-- Functie factorial
fact :: Int -> Int
fact a = if (a == 0) then 1 else fact(a - 1) * a

-- Functie verificare dublu
dublu :: Int -> Int -> Bool
dublu a b = if (a > 2 * b) then True else False

customMax :: [Int] -> Int
customMax [x] = x
customMax (x:remain) = maxim x (customMax remain)

maxim3 x y z = 
  if (x > y) 
    then 
      if (x > z) 
        then x 
        else z
    else 
      if (y > z) 
        then y 
        else z

maxim4 :: (Int, Int) -> (Int, Int) -> Int
maxim4 (a, b) (c, d) = maxim (maxim a b) (maxim c d)

factori :: Int -> [Int]
factori n = [x | x <- [1..n], n `mod` x == 0]

prim :: Int -> Bool
prim n = 
  if length (factori n) == 2
    then True
  else False

numerePrime :: Int -> [Int]
numerePrime n = [x | x <- [2..n], prim x == True]

myzip3 :: [Int] -> [Int] -> [Int] -> [(Int, Int, Int)]
myzip3 (x : xs) (y : ys) (z : zs) = (x, y, z) : myzip3 xs ys zs
myzip3 _ _ _ = []

firstEl :: [(Int, Int)] -> [Int]
firstEl list = map fst list

sumList :: [[Int]] -> [Int]
sumList list = map sum list

customFunct :: Int -> Int
customFunct x = 
  if x `mod` 2 == 0
      then x `div` 2
  else x * 2

pre12 :: [Int] -> [Int]
pre12 list = map customFunct list

charContains :: Char -> [[Char]] -> [[Char]]
charContains character list = filter (elem character) list


patrat :: Int -> Int
patrat x = x * x

impare :: Int -> Bool
impare x = 
  if x `mod` 2 == 0
    then False
  else True 

patrateImpare :: [Int] -> [Int]
patrateImpare list = map patrat (filter impare list)

customFilterZip :: (Int, Int) -> Bool
customFilterZip tuple = 
  if (fst tuple) `mod` 2 == 0
    then False
  else True

listaPatratePozImpare :: [Int] -> [Int]
listaPatratePozImpare list = map patrat (map snd (filter customFilterZip (zip [0..] list)))

main :: IO()
main = do
  print(listaPatratePozImpare [1, 2, 3, 4, 5, 6, 7])
