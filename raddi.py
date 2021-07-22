import pafy
v = pafy.new("https://www.youtube.com/watch?v=TzcHbGNO_Vs")
a = v.audiostreams[-1]
print(a.url)