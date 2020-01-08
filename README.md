# polygon_count
## Description
This repository contains an implementation of an algorithm for polygon counting in line arraignment proposed by M. Fink et al. [1]. The proposed method relies on Bentley–Ottmann algorithm [2] for finding intersections in an arrangement of line segments.
## Example usage
```python
import polygon_count as pc
# Arrangement of lines
A = [((0, 1), (13, 16)),
     ((13, 2), (0, 2)),
     ((13, 5), (0, 8)),
     ((11, -5), (11, 16)),
     ((0, 12), (13, -5)),
     ((8, 12), (12, -6)),
     ((13, 7), (0,7))]
count, ps, isects, G, Q=pc.polygon_count(A)
# visualisation
flags = {
    "input": True,
    "graph": False,
    "result": False,
    "verbose": True
}
pc.show(A, ps, isects, G, Q, flags,count)
```


## References
 [1] Fink, M., Kumar, N., & Suri, S. (2016, August). Counting Fink, M., Kumar, N., & Suri, S. (2016, August). Counting Convex k-gons in an Arrangement of Line Segments. In CCCG (pp. 155-160)Convex k-gons in an Arrangement of Line Segments. In CCCG (pp. 155-160)
 
 [2] Bentley, J. L., & Ottmann, T. A. (1979). Algorithms for reporting and counting geometric intersections. IEEE Transactions on computers, (9), 643-647.