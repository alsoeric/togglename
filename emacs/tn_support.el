;; support file for toggle name functions when interacting with Emacs environment.


(defun write-region-clippy ()
  ""
  ;; write region to a file
  (write-region
   (region-beginning) 
   (region-end)
   "~/tn_clippy.txt"
   )
)

(defun write-clippy ()
  "write last kill ring entry"
  (interactive)
  (with-temp-buffer (yank)(write-region-clippy)))

(defun read-clippy ()
  ""
  (interactive)
  (insert-file-contents 
      "~/tn_clippy.txt"
      )
)

(defun use-this-region-pre()
  "follow with toggle-name-post"
  (py-kill-region
   (region-beginning) 
   (region-end)
   )
  (write-clippy)
  )

(defun toggle-name-pre()
  "follow with toggle-name-post"
  (insert "\C-a")
  (kill-whole-line)
  (write-clippy)
  )

(defun toggle-name-post () 
  ""
  ;;narrow on the empty region at cursor, then readclippy into the narrowed region
  (narrow-to-region    
    (region-beginning) 
    (region-end)
    )
  (read-clippy)  ;;(yank) ;; overwrites active region: yes it does
  ;; search for C-a and stop
  (search-forward "\C-a")
  (delete-backward-char 1)
  )

(defun toggle-statement-pre () 
  "follow with toggle-post"
  (py-kill-statement)
  (write-clippy)
  )

(defun toggle-expression-pre () 
  "follow with toggle-post"
  (py-kill-expression)
  (write-clippy)
  )

(defun toggle-class-pre () 
  "follow with toggle-post"
  (py-kill-class)
  (write-clippy)
  )

(defun toggle-def-pre () 
  "follow with toggle-post"
  (py-kill-def)
  (write-clippy)
  )

(defun toggle-post () 
  ""
   (narrow-to-region    
    (region-beginning) 
    (region-end)
    )
   (read-clippy)  ;; (yank) ;; overwrites active region ??
   )

(defun fix-pre ()
  "common fix code. works in narrowed region"
  (kill-region (point-min) (point-max))
  (write-clippy)
  )

(defun fix-cleanup ()
   ""
   (read-clippy)   ;; (yank)
   ;; search forward for cursor marker
   (beginning-of-buffer)
   (search-forward "\C-a" nil t)
   (delete-backward-char 1)		  
   )



;; Emacs toggle Shell commands

(setq toggleShellCommand  "python c:\\Users\\Tonis\\Documents\\GitHub\\togglename\\vocola\\extensions\\vocola_ext_togglename.py ")

(concatenate 'string toggleShellCommand " -m")

(defun toggle-clippy () 
  "Toggles tn_clippy s2c true, cn false"
  (interactive)
  (shell-command (concatenate 'string toggleShellCommand " -m ct"))
)

(defun toggle-clippy-reverse ()
  "does a reverse toggle on tn_clippy"
  (interactive)
  (shell-command (concatenate 'string toggleShellCommand " -m cr"))
)

(defun toggle-clippy-cursor ()
  "does a reverse toggle on tn_clippy"
  (interactive)
  (shell-command (concatenate 'string toggleShellCommand " -m ct -c"))
)


(defun toggle-clippy-reverse-cursor ()
  "does a reverse toggle on tn_clippy"
  (interactive)
  (shell-command (concatenate 'string toggleShellCommand " -m cr -c"))
)


(defun fixunknwn-clippy ()
  "does a reverse toggle on tn_clippy"
  (interactive)
  (shell-command (concatenate 'string toggleShellCommand " -m cf"))
)


(defun toggle-name ()
  "toggles the name at the cursor"
  (interactive)
  (toggle-name-pre)
  (toggle-clippy-cursor)
  (toggle-name-post)
)


(defun toggle-statement ()
  "toggles the statment"
  (interactive)
  (toggle-statement-pre)
  (toggle-clippy)
  (toggle-post)
)


(defun toggle-expression ()
  "toggles the expression"
  (interactive)
  (toggle-expression-pre)
  (toggle-clippy)
  (toggle-post)
)

(defun toggle-class ()
  "toggles the class"
  (interactive)
  (toggle-expression-pre)
  (toggle-clippy)
  (toggle-post)
)


(defun toggle-def ()
  "toggles the method/function at the cursor"
  (interactive)
  (toggle-def-pre)
  (toggle-clippy)
  (toggle-post)
)


(defun fix-region ()
  "toggles the region and moves the cursor forward at the cursor"
  (interactive)
  (fix-pre)
  (fix-unknown-clippy)
  (fix-post)
)

;; toggle keybindings

;(global-set-key (kbd "C-x t") 'toggle-name)
;(global-set-key (kbd "C-x t d") 'toggle-def)





