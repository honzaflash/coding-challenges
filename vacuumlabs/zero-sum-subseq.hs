import System.Environment ( getArgs )
import Control.Exception
import System.Exit
import System.IO
import Data.List
-- whoops subsequences doesn't do continuous subsequences



readInput :: FilePath -> IO String
readInput = handleFatalIO "Couldn't open input file" . readFile


parseInput :: String -> [[Int]]
parseInput inputStr =
    dropCaseCounts $ map parseIntList $ lines inputStr


-- | converts the sequence of numbers from a String to a list of Ints
-- will explode if not valid integers
parseIntList :: String -> [Int]
parseIntList = map read . words


-- | throws away counts, should/could be rewritten into actually checking them
dropCaseCounts :: [[Int]] -> [[Int]]
dropCaseCounts = dropEvenElems . tail
    where
        dropEvenElems [] = []
        -- this is exhaustive if the input is correct 
        dropEvenElems (a1 : a2 : as) = a2 : dropEvenElems as


-- | decide whether a sequence of integers contains
--   a subsequence with sum of zero
decideZeroSumSubseq :: [Int] -> Bool
decideZeroSumSubseq = any isZeroSum . subsequences'
    where
        isZeroSum = (0 ==) . sum


subsequences' :: [Int] -> [[Int]]
subsequences' = concatMap subinits . subtails 


subtails :: [Int] -> [[Int]]
subtails [] = []
subtails (a : as) = (a : as) : subtails as


subinits :: [Int] -> [[Int]]
subinits = subtails . reverse


printOutput :: [Bool] -> IO ()
printOutput = handleFatalIO "Couldn't open output file" . 
    writeFile "output.txt" . intercalate "\n" . map yesno
    where
        yesno True = "yes"
        yesno False = "no"


-- | used to handle fatal errors
handleFatalIO :: String -> IO a -> IO a
handleFatalIO msg expr = expr `catch` (\e -> do
                                               hPrint stderr (e :: SomeException)
                                               die msg
                                      )


-- | main function
main :: IO ()
main = do
    args <- getArgs
    if length args == 1
        then do
            sequneces <- parseInput <$> readInput (head args)
            printOutput $ map decideZeroSumSubseq sequneces
        else die "usage: zero-sum-subseq FILE"


