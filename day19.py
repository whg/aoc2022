import re
from dataclasses import dataclass, fields
from copy import deepcopy
from multiprocessing import Pool
from functools import partial


@dataclass
class Blueprint:
    number: int
    ore_robot_ore: int
    clay_robot_ore: int
    obsidian_robot_ore: int
    obsidian_robot_clay: int
    geode_robot_ore: int
    geode_robot_obsidian: int


@dataclass
class Count:
    ore: int = 0
    clay: int = 0
    obsidian: int = 0
    geode: int = 0


@dataclass
class State:
    time: int = 1
    robots: Count = Count()
    counts: Count = Count()
    limits: Count = Count(ore=4, clay=9, obsidian=6)
    build_ore: bool = True
    build_clay: bool = True
    build_obsidian: bool = True

    @property
    def key(self):
        return (self.time, self.robots.ore, self.robots.clay, self.robots.obsidian,
                self.counts.ore, self.counts.clay, self.counts.obsidian)


def parse(line):
    return Blueprint(*map(int, re.findall(r'(\d+)', line)))


def run_wrap(bp, end_time=25, state=None):
    max_geodes = 0
    visited = set()
    iterations = 0

    def run(bp: Blueprint, s: State, start_time):
        nonlocal max_geodes, iterations, visited

        if start_time >= end_time:
            return

        key = s.key
        if key in visited:
            return
        visited.add(key)

        iterations += 1

        def update(s):
            for f in fields(s.robots):
                setattr(s.counts, f.name, getattr(s.counts, f.name) + getattr(s.robots, f.name))

        for t in range(start_time, end_time):
            s.time = t
            if s.build_ore and s.robots.ore < s.limits.ore and s.counts.ore >= bp.ore_robot_ore:
                ss = deepcopy(s)
                update(ss)
                ss.counts.ore -= bp.ore_robot_ore
                ss.robots.ore += 1
                ss.build_clay = ss.build_obsidian = True
                run(bp, ss, t + 1)
                s.build_ore = False

            if s.build_clay and s.robots.clay < s.limits.clay and s.counts.ore >= bp.clay_robot_ore:
                ss = deepcopy(s)
                update(ss)
                ss.counts.ore -= bp.clay_robot_ore
                ss.robots.clay += 1
                ss.build_ore = ss.build_obsidian = True
                run(bp, ss, t + 1)
                s.build_clay = False

            if (s.build_obsidian and s.robots.obsidian < s.limits.obsidian
                    and s.counts.ore >= bp.obsidian_robot_ore and s.counts.clay >= bp.obsidian_robot_clay):
                ss = deepcopy(s)
                update(ss)
                ss.counts.ore -= bp.obsidian_robot_ore
                ss.counts.clay -= bp.obsidian_robot_clay
                ss.robots.obsidian += 1
                ss.build_ore = ss.build_clay = True
                run(bp, ss, t + 1)
                s.build_obsidian = False

            build_geode = False
            if s.counts.ore >= bp.geode_robot_ore and s.counts.obsidian >= bp.geode_robot_obsidian:
                s.counts.ore -= bp.geode_robot_ore
                s.counts.obsidian -= bp.geode_robot_obsidian
                build_geode = True
                s.build_obsidian = True

            update(s)

            if build_geode:
                s.robots.geode += 1

            max_geodes = max(s.counts.geode, max_geodes)

    if state is None:
        state = State(robots=Count(ore=1), counts=Count())
    run(bp, state, state.time)

    return max_geodes


blueprints = list(map(parse, open('day19.txt')))

with Pool(6) as pool:
    max_geodes = pool.map(run_wrap, blueprints)
a = sum(g * bp.number for g, bp in zip(max_geodes, blueprints))

func_b = partial(run_wrap, end_time=33, state=State(robots=Count(ore=1), counts=Count(), limits=Count(ore=3, clay=10, obsidian=10)))
with Pool(3) as pool:
    bs = pool.map(func_b, blueprints[:3])

print(a, bs[0] * bs[1] * bs[2])
