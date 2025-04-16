(define (curry-cook formals body) 
(if (null? formals)
body  ; 如果没有参数了，返回 body
(let ((param (car formals)))  ; 获取第一个参数
  (list 'lambda (list param)  ; 返回一个新的 lambda
        (curry-cook (cdr formals) body)))))  ; 递归处理剩余的参数)

(define (curry-consume curry args)
  'YOUR-CODE-HERE)

(define-macro (switch expr options)
  (switch-to-cond (list 'switch expr options)))

(define (switch-to-cond switch-expr)
  (cons _________
        (map (lambda (option)
               (cons _______________ (cdr option)))
             (car (cdr (cdr switch-expr))))))
