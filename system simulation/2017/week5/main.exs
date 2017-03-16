defmodule Foo do
  def sim(a, t , v, r, n), do: _sim [v], a, t, r, n
  defp _sim(list, _, _, _, 0), do: list
  defp _sim(list = [head | tail], a, t, r, n), do: _sim([ cylinder(a, t, head, r) | list], a, t, r, n - 1)

  defp cylinder(a, t, v, r), do: v - (a * t * v / (:math.pi * :math.pow(r, 2)))
  defp cone(a, t, v, r), do: v - (a * t * v / (:math.pi * :math.pow(r, 2)))

  def cylindervolume(r, h), do: :math.pi * (:math.pow r, 2) * h
end

a1 = 1.0
h1 = 0
r1 = 1.0

IO.inspect Foo.sim(1.0, 0.1, Foo.cylindervolume(1.5/2, 2.5), 1.5/2, 50)
