import Blog2
from Security2 import Security2
from Blog2 import Blog2

sec = Security2("botbreaker")
sec.loadCredentials()

blog = Blog2(sec)

# quit()

pass_record = "PASSED:\n"
fail_record = "FAILED:\n"

print("INFO CHECK...")
print("TESTING INFO PASS CASES.")
print("INFO TEST P001:")
print(blog.info("botbreaker"))

print("INFO TEST P002:")
print(blog.info("botbreaker", ["name"]))

print("INFO TEST P003:")
print(blog.info("botbreaker", []))

print("INFO PASS CASES PASSED.")

print("INFO PASSED.")
pass_record += "INFO PASSED.\n"

print("REPORT:")
print(pass_record)
