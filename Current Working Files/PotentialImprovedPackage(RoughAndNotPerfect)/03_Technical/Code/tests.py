"""Small deterministic checks; run with python -m unittest tests -v."""
import unittest
import numpy as np
from growth import surface,field,spacing,simulate,RADIUS
from analyze_export import segment_distances,tube

class GeometryTests(unittest.TestCase):
    def test_cylinder(self):
        p=surface(np.array([[-.6,0],[0,1],[.6,1.8]]))
        np.testing.assert_allclose(np.sqrt(p[:,0]**2+(p[:,1]-RADIUS)**2),RADIUS,atol=1e-12)
    def test_intrinsic_metric(self):
        a=np.array([[.17,.82]]);h=1e-6
        du=(surface(a+[h,0])-surface(a))/h;dv=(surface(a+[0,h])-surface(a))/h
        self.assertAlmostEqual(np.linalg.norm(du),1,places=7);self.assertAlmostEqual(np.linalg.norm(dv),1,places=7)
        self.assertAlmostEqual(float((du*dv).sum()),0,places=7)
    def test_field_bounds(self):
        p=np.array([[0,1.16],[-.6,0],[.6,1.8]])
        for mode in ['uniform','gradient','focused']:
            f=field(p,mode);self.assertTrue(np.all((f>=0)&(f<=1)))
            self.assertTrue(np.all((spacing(p,mode)>=.030)&(spacing(p,mode)<=.056)))
    def test_crossing_segments(self):
        d=segment_distances(np.array([[-1.,0,0]]),np.array([[1.,0,0]]),np.array([[0,-1.,0]]),np.array([[0,1.,0]]))
        self.assertAlmostEqual(float(d[0]),0)
    def test_parallel_segments(self):
        d=segment_distances(np.array([[0.,0,0]]),np.array([[1.,0,0]]),np.array([[0.,1,0]]),np.array([[1.,1,0]]))
        self.assertAlmostEqual(float(d[0]),1)
    def test_cyclic_mesh(self):
        t=np.linspace(0,2*np.pi,50,endpoint=False);p=np.column_stack((np.cos(t),np.sin(t),t*0))
        self.assertTrue(tube(p,.02).is_watertight)
    def test_repeatability(self):
        a,_,_=simulate('focused',17,60);b,_,_=simulate('focused',17,60)
        np.testing.assert_array_equal(a,b)

if __name__=='__main__':unittest.main()
