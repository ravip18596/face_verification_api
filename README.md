# Deep Learning based Face Verification REST Api

## RUN
```
python main2.py

```


## ADD FACE
```
curl -X POST -F image=@images/rishabh.png 'http://localhost:5000/add?name=rishabh'

```

## Verify FACE
```
curl -X POST -F image=@images/rishabh.png 'http://localhost:5000/verify?name=rishabh'
```
