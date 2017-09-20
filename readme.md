## Tsinghua Course Selector
比起原版TCS加入了

1. 多课程选取（2s一次轮询）
2. 每次login的session可以多次选课，提示掉线后会自动重新login
3. patience机制（可以多开进程，某个进程陷入频繁需要获取验证码时，会自动重新login）

仍然还是会有选上课后会继续尝试选取的问题，就当feature好了...