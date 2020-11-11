# PasswordPandemonium Writeup

This is a pretty simple challenge. You have to find a password that meets the requirements below:

- Minimum length of 8
- Maximum length of 32
- Must include at least one letter
- Must include >= 2 special characters
- Must include a prime amount of numbers
- Must have even amount of capital and lowercase characters
- Must include an emoji
- MD5 hash must start with a number
- Must be valid JavaScript that evaluates to True
- Must be JavaScript that does not evaluate to a String
- Must be a palindrome

This challenge should be pretty self-explanatory. The only thing that may be worth noting are the
last two requirements, which the following should be noted:

- This challenge uses [QuickJS](https://bellard.org/quickjs/quickjs.html) to validate JavaScript.
While most JavaScript features should be supported, some methods like `console.log` and all DOM
operations are not considered valid. However, those solutions wouldn't be valid anyways, as they
wouldn't likely evaluate to True.
- `1` is evaluated as True, as are strings.
- To make the password palindromic, you can abuse inline comments.

Some possible solutions include:

- `(_=>(1))()//Xx🐬xX//)())1(>=_(`
- `1//Ab✔bA//1`
- `()=>{}//Ab1👋1bA//}{>=)(`

Submitting a valid password (and a non-empty username) will reveal the flag. Otherwise, the most
"minor" invalid rule would be displayed to the user.