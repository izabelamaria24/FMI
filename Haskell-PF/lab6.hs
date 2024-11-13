
data Fruct
  = Mar String Bool
  | Portocala String Int

cosFructe = [Mar "Ionatan" False,
            Portocala "Sanguinello" 10, 
            Portocala "Valencia" 22,
            Mar "Golden Delicious" True,
            Portocala "Sanguinello" 15,
            Portocala "Moro" 12,
            Portocala "Tarocco" 3,
            Portocala "Moro" 12,
            Portocala "Valencia" 2,
            Mar "Golden Delicious" False,
            Mar "Golden" False,
            Mar "Golden" True]

ePortocalaDeSicilia :: Fruct -> Bool
ePortocalaDeSicilia (Portocala "Sanguinello" _) = True
ePortocalaDeSicilia (Portocala "Moro" _) = True
ePortocalaDeSicilia (Portocala "Tarocco" _) = True
ePortocalaDeSicilia _ = False

nrFeliiSicilia :: [Fruct] -> Int
nrFeliiSicilia listaFructe = sum [n | Portocala tip n <- listaFructe, ePortocalaDeSicilia(Portocala tip n)]

nrMereViermi :: [Fruct] -> Int
nrMereViermi listaFructe = length [n | Mar tip n <- listaFructe, n]

type NumeA = String
type Rasa = String
data Animal = Pisica NumeA | Caine NumeA Rasa
  deriving Show

vorbeste :: Animal -> String
vorbeste (Pisica _) = "Meow!"
vorbeste (Caine _ _) = "Woof!"


rasa :: Animal -> Maybe String
rasa (Pisica _) = Nothing
rasa (Caine _ rasa_caine) = Just rasa_caine 

main::IO()
main = do
  print(nrFeliiSicilia cosFructe)
  print(nrMereViermi cosFructe)
  print(vorbeste (Pisica "miti"))
  print(rasa(Caine "doggo" "dog"))
  print(rasa(Pisica "cat"))
  
