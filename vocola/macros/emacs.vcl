include Unimacro.vch;
# Voice commands for emacsand at local commands
search (forward={ctrl+s}|back={ctrl+r}) = $1;
yank (again={Esc}y|it back={ctrl+y}) = $1;
# Voice commands for xwin

include Unimacro.vch;
include folders.vch;
include   files.vch;

## 
# (Python="#!/bin/python"|perl="#!/bin/perl"|bash="#!/bin/bash") first line = $1;

# This really should be just for xemacs but, we will do the best we can

# (date | time | log) stamp = stamp.string($1);

search (forward={ctrl+s}|back={ctrl+r}) = $1;
yank (again={Esc}y|it back={ctrl+y}) = $1;
go to line = {Alt+g};
repeat (it={ctrl+u} | twice={ctrl+u2} | thrice={ctrl+u3} ) = $1;
leave mark = {ctrl+shift+2};

copy    (character={esc}xdelete-forward-char{enter}{ctrl+y} | 
         word= {esc}d{ctrl+y}|
         line={esc}xset-mark{ctrl-e}{esc}w
        )= $1;

kill    (character = {ctrl+d} |
         word={esc}d|
         line={ctrl+k}
        )= $1;

delete  (character = {esc}xdelete-backward-charI{enter}|
         word={esc}xbackward-kill-word{enter}|
         line={ctrl+u}0k{}
        )= $1;

left    (character={ctrl+b}|
         word={esc}b|
         line={ctrl+u}0k{esc}xforward-line{enter}
        )= $1;

right   (character={ctrl+f}|
         word={esc}f| add
         line={esc}xforward-line{enter}
        )= $1;


# python extensions might be things like "change comments| sentence | word | paragraph".  

Empty triple quotes = {tab}'""" """';
Empty method definition = ' (self,):'{ctrl+a}{tab}'def ' ;

#
### Toggle name commands

savemp():= {ctrl+x}r{space}z{ctrl+x}{ctrl+x}{ctrl+x}r{space}a;

restoremp() := {ctrl+x}rjz{ctrl+shift+2}{ctrl+x}rja;

restore mark and point = restoremp();

#tncleanup() := (yank)(exchange-point-and-mark)
#	       # search forward for cursor marker
#	       (search-forward "\C-a")(delete-backward-char)
#                ;

(use this|toggle) region = '{esc}:(use-this-region-pre){enter}'
              Wait(0)
              toggle.name(1,0) 
	      '{esc}:(toggle-post){enter}'
	      ;


toggle name = '{esc}:(toggle-name-pre){enter}'
              Wait(0) # wait to flush character queue
              toggle.name(1,1) # string to code, need cursor marker
	      '{esc}:(toggle-name-post){enter}'
	      # CLIPSAVE()/CLIPRESTORE()
	      ;

toggle statement = '{esc}:(toggle-statement-pre){enter}'
              Wait(0)
              toggle.name(1,0)
	      '{esc}:(toggle-post){enter}'
	      # CLIPSAVE()/CLIPRESTORE()
	      ;

toggle expression = '{esc}:(toggle-expression-pre){enter}'
              Wait(0)
              toggle.name(1,0) 
	      '{esc}:(toggle-post){enter}'
	      # CLIPSAVE()/CLIPRESTORE()
	      ;

toggle class = '{esc}:(toggle-class-pre){enter}'
              Wait(0)
              toggle.name(1,0) 
	      '{esc}:(toggle-post){enter}'
	      # CLIPSAVE()/CLIPRESTORE()
	      ;

toggle (definition|method) = '{esc}:(toggle-def-pre){enter}'
              Wait(0)
              toggle.name(1,0) 
	      '{esc}:(toggle-post){enter}'
	      # CLIPSAVE()/CLIPRESTORE()
	      ;


(fix|fixed) region = '{esc}:(fix-pre){enter}'
              Wait(0)
              # fix names and move to next unknown
              toggle.firstunknown() 
	      '{esc}:(fix-cleanup){enter}'
	      ;

# only make on extension call.  region management gets too confusing
(fix|fixed) next = '{esc}:(fix-pre){enter}'
              Wait(0)
	      toggle.fix_unknown()
	      '{esc}:(fix-cleanup){enter}'
	      ;

(fix|fixed) unknown = '{esc}:(fix-pre){enter}'
              Wait(0)
    	      toggle.firstunknown()
	      '{esc}:(fix-cleanup){enter}'
	      ;

all done = '{esc}:(fancy-widen){enter}'
	      ;

fillOther(lchar,rchar) := $rchar{ctrl+x}{ctrl+x}$lchar{ctrl+x}{ctrl+x};

paren that           = fillOther('(',')');
bracket that         = fillOther('[',']');
brace that           = fillOther('{','}');
single [quote]  that = fillOther("'","'");
double [quote]  that = fillOther('"','"');
tripple [quote] that = fillOther('"""','"""');


### 

### add argument = 
# -------
do(command) := {Alt+x} $command {Enter};
elisp(e) := {Alt+:} $e {Enter};

# ---------------------------------------------------------------------------
# Buffer and File Manipulation

Buffer <file>        = {Ctrl+x}{Ctrl+f} $1 {Enter};
Buffer <file> Revert = {Ctrl+x}{Ctrl+f} $1 {Enter}
                       do(revert-buffer) yes{Enter};
Switch Buffer = do(get-next-buffer);
Switch Buffer         1..20 =        {Ctrl+x}{Ctrl+b}{Down_$1} " ";
I Meant Switch Buffer 1..20 = {Alt+o}{Ctrl+x}{Ctrl+b}{Down_$1} " ";
Kill Buffer        = {Ctrl+x}k{Enter};
Two Buffers        = {Ctrl+x}2;
Two Buffers Across = {Ctrl+x}3;
One Buffer         = {Ctrl+x}1;
Other Buffer       = {Ctrl+x}o;
One Other Buffer   = {Ctrl+x}0;
Buffer List        = {Ctrl+x}{Ctrl+b};
Revert Buffer = do(revert-buffer) yes{Enter};
Revert Buffer Hard = {Ctrl+x}{Ctrl+v}{Enter};
Buffer Shell = do(shell);
Buffer (scratch|compilation) = {Ctrl+x}b *$1* {Enter};
[Toggle] Read Only = {Ctrl+x}{Ctrl+q};
[Toggle] Fill Mode = do(auto-fill-mode);
[Toggle] (Overwrite|Overstrike) Mode = do(overwrite-mode);

Open File  = {Ctrl+x}{Ctrl+f};
Save (File={Ctrl+s} | All=s | As={Ctrl+w}) = {Ctrl+x} $1;
Open File <folder> = {Ctrl+x}{Ctrl+f}{Ctrl+a}{Ctrl+k} $1/;
Save As   <folder> = {Ctrl+x}{Ctrl+w}{Ctrl+a}{Ctrl+k} $1/;
Wrong File = {Ctrl+x}{Ctrl+v};
Recover File = do(recover-file) {Enter}yes{Enter};
Make Directory = do(make-directory) {Enter};

Reload Dot Emacs = do(load-library) ~/.emacs{Enter};
(Exit Emacs | Close Window) = {Ctrl+x}{Ctrl+c};

I Meant Edit Machine Commands =
    {Alt+k} SendSystemKeys({Alt+Tab}) HeardWord(Edit, Machine, Commands);

# ---------------------------------------------------------------------------
# Straight mouse grid commands inspired by Kim Patch

include utilities.vch;

<n> := 0..99;
<n> <n> ( Paste     = {Ctrl+y}
        | Mark      = {Ctrl+Space}
        | Copy      = {Alt+w}
        | Kill      = {Ctrl+w}
        | Duplicate = {Alt+w}{Ctrl+y}
        | Kill Line      = {Ctrl+a}{Ctrl+Space}{Ctrl+n}{Ctrl+w}
        | Copy Line      = {Ctrl+a}{Ctrl+Space}{Ctrl+n}{Alt+w}
        | Duplicate Line = {Ctrl+a}{Ctrl+Space}{Ctrl+n}{Alt+w}{Ctrl+y}
        )
     = touch($2,$1) $3;

# ---------------------------------------------------------------------------
# Text Navigation and Editing

<n> (Up | Down | Left | Right) = {$2_$1};

### Generic "Select and Modify"

<edit> := ( Select    = "" 
          | Copy      = {Alt+w}
          | Duplicate = {Alt+w}{Ctrl+y}
          | Kill      = {Ctrl+w}
          );

<edit> ( That         = ""
       | Line         = {Ctrl+a}{Ctrl+Space}{Ctrl+n}   
       | Item         = do(mark-outline-item)
       | Graph        = {Alt+h}                        
       | (Flow | All) = {Ctrl+x}h                      
       ) = $2 $1;

<thing_start> := ( Word          = {Alt+b}
                 | Line          = {Ctrl+a}
                 | Item          = do(outline-item-start)
                 | Graph         = {Esc}{
                 | (Flow|Buffer) = {Alt+<}
                 );
<thing_end>   := ( Word          = {Alt+f}
                 | Line          = {Ctrl+e}
                 | Item          = do(outline-item-end)
                 | Graph         = {Esc}}
                 | (Flow|Buffer) = {Alt+>}
                 );

<thing_start> Start = $1;
<thing_end>   End   = $1;

<edit>      <thing_end>    Here  = {Ctrl+Space} $2 $1;
<edit> Back <thing_start> [Here] = {Ctrl+Space} $2 $1;

### Characters

<edit> (Char | 1) = {Ctrl+Space}{Right} $1;
<edit> <n>        = {Ctrl+Space}{Right_$2} $1;
[Kill] Back <n> = {Esc}$1{Backspace};
(Cap | Up Case) <n> = {Ctrl+Space}{Right_$2} do(upcase-region);
Down Case       <n> = {Ctrl+Space}{Right_$1} do(downcase-region);

### Words

<left_right> := Left={Alt+b} | Right={Alt+f};
  <n> Words <left_right> = {Esc} $1 $2;
[One] Word  <left_right> = $1;

<editword> := ( Kill      = {Alt+d} 
              | Kill Back = {Alt+Backspace}
              | Copy      = {Alt+d}{Ctrl+x}u
              | Cap       = {Alt+c}
              | Up Case   = {Alt+u}
              | Down Case = {Alt+l}
              );
<editword> Word = $1;
<editword> This Word = {Alt+b} $1;
<editword> <n> Words = {Esc} $2 $1;

### Lines

New Line = {Enter};
Newline Indent = {Ctrl+j};
Line Here = {Ctrl+o};
(Paragraph | Graph) Here = {Ctrl+o}{Ctrl+o};
Open Line = {Enter}{Ctrl+o};
Join Line = {Ctrl+u} do(delete-indentation);
Join Line <n> = {Ctrl+t_$1};

Line (Down|Up)     = {Ctrl+a}{Ctrl+Space}{Ctrl+n}{Ctrl+w}{$1}   {Ctrl+y}{Up};
Line (Down|Up) <n> = {Ctrl+a}{Ctrl+Space}{Ctrl+n}{Ctrl+w}{$1_$2}{Ctrl+y}{Up};
Move to Line <n>   = {Ctrl+a}{Ctrl+Space}{Ctrl+n}{Ctrl+w}{Ctrl+x}rmTemp{Enter}
                     touch(0,$1) {Ctrl+y}{Ctrl+x}rbTemp{Enter}{Ctrl+x}o;

<edit>      Here = {Ctrl+Space}{Ctrl+e} $1;
<edit> Back Here = {Ctrl+Space}{Ctrl+a} $1;

<edit>      <n> Lines = {Ctrl+a}{Ctrl+Space}{Esc} $2 {Ctrl+n} $1;
<edit> Back <n> Lines = {Ctrl+a}{Ctrl+Space}{Esc} $2 {Ctrl+p} $1;

### Paragraphs

Graph (Start="{" | End="}") <n> = {Esc} $2 {Esc} $1;
Fill Graph = {Alt+q};
Fill Graph Here = ButtonClick() {Alt+q};

<edit>      <n> Graphs = {Esc} $2 {Esc}} {Ctrl+Space}{Esc} $2 {Esc}{ $1;
<edit> Back <n> Graphs = {Esc} $2 {Esc}{ {Ctrl+Space}{Esc} $2 {Esc}} $1;

### Copy/Paste

Paste That = {Ctrl+y};
Paste Here = ButtonClick() {Ctrl+y};
Yank  That = {Ctrl+y};
Yank Again = {Alt+y};

Set Mark = {Ctrl+Space};
[Set] Mark Here = ButtonClick() {Ctrl+Space};
Switch Mark = {Ctrl+x}{Ctrl+x};

Copy  To   <n> = do(copy-to-register) $1;
Paste From <n> = do(insert-register)  $1;

(Kill=k | Paste=y | Clear=c | Open=o) Box = {Ctrl+x}r $1;
Copy Box = {Alt+J};

Replace All = {Alt+<}{Ctrl+y}{Ctrl+Space}{Alt+>}{Ctrl+w};
Copy and Switch        = {Ctrl+x}h{Alt+w} Wait(0) SendSystemKeys({Alt+Tab});
Copy and Switch Buffer = {Ctrl+x}h{Alt+w} do(get-next-buffer);
Copy to Natspeak       = {Ctrl+x}h{Alt+w} AppBringUp(NatSpeak);

### Indenting
Indent   <n> = {Esc}   $1 {Ctrl+x}{Ctrl+i};
(out dent | Unindent) <n> = {Esc} - $1 {Ctrl+x}{Ctrl+i};
Indent Region = do(indent-region);
Indent <n> Lines = {Ctrl+a}{Ctrl+Space}{Down_$1} do(indent-region);


# ---------------------------------------------------------------------------
# Navigation

### Scrolling
Center Cursor = {Ctrl+l};
Page (Up=PgUp | Down=PgDn)     = {$1};
Page (Up=PgUp | Down=PgDn) <n> = {$1_$2};
Scroll (up|down) <n> = {Esc} $2 do(scroll-$1);

### Line Numbers
<digit> := 0..9;
Line Number = {Alt+Shift+g};
Line [Number] <digit> = {Alt+Shift+g} $1 {Enter};
Line [Number] <digit> <digit> = {Alt+Shift+g} $1 $2 {Enter};
Line [Number] <digit> <digit> <digit> = {Alt+Shift+g} $1 $2 $3 {Enter};
Line [Number] <digit> <digit> <digit> <digit> = {Alt+Shift+g}$1$2$3$4{Enter};
What Line = do(what-line);

### Search/Replace
Find Down = {Ctrl+s};
Find Up   = {Ctrl+r};
Find Again [Down] = {Ctrl+s}{Ctrl+s};
Find Again Up     = {Ctrl+r}{Ctrl+r};
Find (Word|That) [Down] = {Ctrl+s}{Ctrl+w}{Ctrl+s};
Find (Word|That)  Up    = {Ctrl+r}{Ctrl+w}{Ctrl+r};
Find <n> Words [Down] = {Ctrl+s}{Ctrl+w_$1}{Ctrl+s};
Find <n> Words  Up    = {Ctrl+r}{Ctrl+w_$1}{Ctrl+r};
Replace String = do(replace-string);
Query Replace = {Esc}%;
Query Replace Regular Expression = do(query-replace-regexp);
Replace Regular Expression = do(replace-regexp);

### Bookmarks
Bookmark List = do(edit-bookmarks);
Set Bookmark        = {Ctrl+x}rm;
Enter Bookmark      = {Ctrl+x}h{Alt+w}{Ctrl+x}rbBookmarks{Enter};
Set Bookmark <n>    = {Ctrl+x}rm $1 {Enter};
Clear Bookmark <n>  = do(bookmark-delete) $1 {Enter};
Bookmark     <n>    = {Ctrl+x}rb $1 {Enter};

### Miscellaneous
Undo That = {Ctrl+x}u;
Undo <n> = {Esc} $1 do(undo);
Abort That = {Ctrl+g};
Say (yes|no) = $1 {Enter};
Kill Space = {Esc}\;
One Space = {Alt+Space};
Macro (Start="(" | Stop=")" | Do=e) = {Ctrl+x} $1;
Macro (Do|Execute|Run) 1..5 = {Ctrl+u_$2}{Ctrl+x}e;
(Sort|Keep|Flush) Lines = do($1-lines);
Hide <n> = {Esc} $1 {Ctrl+x}$;
Perl Region = do(perl-region);

Search Files = do(grep);
Find Tag = {Alt+.}{Enter};
Tag Search = {Ctrl+Space}{Alt+f}{Alt+w} do(tags-search) {Ctrl+y};
Complete (Name|Word|Tag) = {Alt+/};

Camel <n> = {Alt+b_$1}{Alt+f} Repeat(Eval($1-1), {Ctrl+d}{Alt+c});

# Defining these here allows using them in command sequences
include keys.vch;  

# ---------------------------------------------------------------------------
# Context-Sensitive Commands

### Editing Vocola files
.vcl | .vch:
  Insert ( Control Key = {Ctrl+
         | Alt Key     = {Alt+
         | Wait        = " Wait(100)"
         ) = $1;
  Insert             <key> = {$1       Wait(0) };     # see keys.vch 
  Insert       <mod> <key> = {$1+$2    Wait(0) };
  Insert <mod> <mod> <key> = {$1+$2+$3 Wait(0) };

### Programming in various languages

.pl | .pm | .py | .java | .cpp | .h:
  Statement (Start="" | Down={Ctrl+n} | Up={Ctrl+p}) = $1 {Ctrl+a}{Ctrl+i};
  New Statement       = {Ctrl+e}        {Ctrl+j};
  New Statement Above = {Ctrl+a}{Ctrl+b}{Ctrl+j};
  New Block = {Ctrl+e}{Ctrl+j}{{Ctrl+j_2}}{Up}{Tab};
.pl | .pm | .py:
  New Comment       = {Ctrl+e}        {Ctrl+j} "# ";
  New Comment Above = {Ctrl+a}{Ctrl+b}{Ctrl+j} "# ";
.java | .cpp | .h:
  New Comment       = {Ctrl+e}        {Ctrl+j} "// ";
  New Comment Above = {Ctrl+a}{Ctrl+b}{Ctrl+j} "// ";

.pl | .pm :
  Insert Hash Reference = ->{}{Ctrl+b};
  Insert Subroutine = "{Enter}sub {Enter}{{Enter 2}}{Enter}{Ctrl+b 6}";

.cpp:
  Open Header [File] = "{Alt+:}(kill-new buffer-file-name){Enter}"
                       {Ctrl+x}{Ctrl+f}{Ctrl+y}{Backspace_3}h{Enter};

### Editing HTML files
.html | .htm:
  Show Preview = {Ctrl+x}{Ctrl+s} elisp("(kill-new buffer-file-name)")
                 AppBringUp(iexplore) {Alt+d}{Ctrl+v}{Enter}
                 Wait(100) AppBringUp(Emacs);
  Heading 1..6 = {Ctrl+a}<h$1>{Ctrl+e}</h$1>;

### Shell Commands
*shell*:
  Folder <folder> = "cd $1" {Ctrl+a}{Alt+:}
                    '(replace-string "\\" "/"){Enter}{Enter}';
  Go Up = "cd ..{Enter}";
  Go Up <n> = "cd " Repeat($1, ../) {Enter};
  Command (Up=p | Down=n) = {Alt+$1};
  Command (Up=p | Down=n) Go = {Alt+$1}{Enter};
  Command (Up=p | Down=n) 1..30 = {Alt+$1_$2};
  Command (Up=p | Down=n) 1..30 Go = {Alt+$1_$2}{Enter};

### Compilation Commands
*compilation*:
  First Error = {Shift+Alt+<}{Alt+n};
  Error (Up=p | Down=n) = {Alt+$1};
  Error (Up=p | Down=n) Go = {Alt+$1}{Enter};
  Error (Up=p | Down=n) 1..30 = {Alt+$1_$2};
  Error (Up=p | Down=n) 1..30 Go = {Alt+$1_$2}{Enter};

