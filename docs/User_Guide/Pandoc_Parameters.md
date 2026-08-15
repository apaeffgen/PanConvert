# Extenden Parameters

In the manual converter tab, there is an input field for manual parameters.
All Pandoc parameters can be used. But these rules have to be applied.
Non text formats like .odt need to be saved with the --output parameter.

- Only short parameters without blanks work
- Only the long parameters can always be concatenated 
- Parameters have to be concatenated by semicolon
- No blanks are allwowed in the concatenation.

Examples that work: 
--standalone;--output=/home/User/Documents/test.html
-s;--output=/home/User/Documents/test.html
--output=/home/User/Documents/test.odt


Examples that fail:
-s;-o /home/User/Documents/test.html
-o /home/User/Documents/test.html