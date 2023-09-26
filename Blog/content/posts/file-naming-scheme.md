---
title: "Personal File Naming Scheme(s)"
date: 2023-09-23T19:54:13+02:00
draft: false
---

To keep your filesystem from becoming a mess, I think it's important to decide on a naming scheme to use for your files.
This is very similar to using a style guide for formatting source code when programming.
You decide on a set of rules, and stick to them.
These rules can be as simple or complicated as you wish.

There's essentially only two considerations:

1. How Linux interacts with names; for instance on the command line and when writing scripts.
2. How names are most easily understood by humans.

Unfortunately, these two points are often in conflict.
The quintessential example of this is spaces.
The most natural way to represent spacing in names for a human is just that, a blank space.
However, the space is also used to separate argument on the command line.
Therefore, you have to escape spaces when typing commands, which is annoying.
The same goes for scripting.

The aim therefore is to strike a balance between readability and "type"-ability.
To that end, I've come up with the following rules.

1. File names can only include upper- and lowercase English alphabet; that is A-Z and a-z, as well as the numbers 0-9, and the special characters hyphen, underscore, and period.
2. Do not use file extensions if they are not necessary.
   The prime culprit here is .txt.
   File extensions are for the benefit of the human, not the computer.
3. Directories are named using PascalCase.
4. Regular files are named using kebab-case. (I.e. all lowercase
   with hyphens as a delimiter between words.)

In addition to this I think it's useful to also invent schemas for different types of media.
For instance, when storing pdfs of books how should the name be formatted?
The key consideration here is if, and where, to put the author(s) and publishing year.
Let's make up a book title: "The Book Title" by "Author Anderson" and "Author Banderson", published in 1984.

The title should come first, so the name starts out as `the-book-title`.
After this we put an underscore as a delimiter followed by the author(s) last name(s) separated by hyphens:
`the-book-title_anderson-banderson` and then finally another underscore as a delimiter and then the full year of publication.
We also include an extension to show that this is a pdf document:

`the-book-title_anderson-banderson_1984.pdf`.

A real book rendered like this could be:

`analysis-ii_tao_2015.pdf`

The question of editions and printings is dealt with by including the publishing year.

Articles and essays are named in the same way.

Similarly one should construct a naming schema for other types of media that are dealt with often.
Examples of these are: movies, music, pictures, and so on.
I do not store any large amount of these types of media, but you should be able to come up with good systems for these yourself.
