;; support file for toggle name functions when interacting with Emacs environment.

(defun tncleanup (
		  (exchange-point-and-mark)
		  ;; search forward for cursor marker
		  (search-forward "\C-a")
		  (delete-backward-char 1)
		  )
)

(defun toggle-statement (
			 (py-kill-statement)
			 (shell-command "tnshell -mt")
              toggle.name(1,0) 
	      {ctrl+y}
              savemp();
	      # CLIPSAVE()/CLIPRESTORE();

tn_support.el
tn_support.el~
(shell-command "ls" t)tn_support.el
tn_support.el~

