
verifL :: [Int] -> Bool
verifL = even . length

zipLeftover :: [a] -> [a] -> [a]
zipLeftover []     []     = []
zipLeftover xs     []     = xs
zipLeftover []     ys     = ys
zipLeftover (x:xs) (y:ys) = zipLeftover xs ys

lastN :: Int -> [a] -> [a]
lastN n xs = zipLeftover (drop n xs) xs

remove :: Int -> [Int] -> [Int]
remove n l = take (n - 1) l ++ drop n l

myreplicate :: Int -> Int -> [Int]
myreplicate n v = take n (repeat v)

sumImp :: [Int] -> Int
sumImp l = sum (filter odd l)

totalLength :: [String] -> Int
totalLength = sum (length (filter (strStartsWith 'a')))

testSum :: [Int] -> Int
testSum l = sum((x `mod` 2 ) * x)


main :: IO()
main = do
  print(testSum [1, 2, 3, 4, 5])
