import random
def shortest_time_remaining(processes=[]):
  arrival_times = sorted(set(map(lambda (a,b,c,d): c, processes)))
  currently_running = None
  quantums = 0
  while True:
    if (len(arrival_times) and quantums == arrival_times[0]):
      arrival_times = arrival_times[1:]
      if currently_running:
        processes.append(currently_running)
      currently_running = None

    if not currently_running:
      available_processes = [(a,b,c,d) for (a,b,c,d) in processes if c <=
        quantums]
      if available_processes:
        currently_running = min(available_processes, key = lambda (a,b,c,d): d)
        processes.remove(currently_running)
      else:
        print "No processes running at time", quantums
        quantums += 1
        continue

    name, user, starttime, remaining = currently_running
    remaining -= 1

    print "At time %i" % int(quantums),
    print name, "remaining time:", remaining

    if remaining:
      currently_running = (name, user, starttime, remaining)
    else:
      currently_running = None
      print "process %s has finished" % name

    quantums +=1

    if currently_running == None and len(processes) == 0:
      break

def lottery(processes=[], priorities=[]):
  box = []
  for (name, owner, starttime, remaining) in processes:
    username, priority = filter(lambda (a,b): a==owner, priorities)[0]
    box += [(name, starttime)]*priority
  quantums = 0
  while True:
    available = filter(lambda (a,b): b <= quantums, box)
    if available:
      index = random.randrange(len(available))
      name, starttime = available[index]
      name, user, starttime, remaining =\
        filter(lambda (a,b,c,d): a == name, processes)[0]
      remaining -= 2
      remaining = remaining >= 0 and remaining or 0
      processes = filter(lambda (a,b,c,d): a != name, processes)
      if remaining > 0:
        processes.append((name, user, starttime, remaining))
        next_quantum = quantums + 2
      else:
        box = filter(lambda (a,b): a != name, box)
        next_quantum = quantums + 1
      print "From time %i to %i: %s remaining time: %i" % (quantums,
      next_quantum, name, remaining)
      quantums = next_quantum
      if remaining <= 0:
        print "Process %s has finished" % name
      if not processes:
        break
    else:
      print "No processes are running at time %i" % quantums
      quantums += 1

def fair_share(processes=[], priorities=[]):
  user_queues = []
  ballot = []
  for (owner, priority) in priorities:
    queue = filter(lambda (a,b,c,d): b == owner, processes)
    # queue = map(lambda (a,b,c,d): (a,c), queue)
    user_queues.append((owner, queue))
    ballot += [owner] * priority
  random.shuffle(ballot)

  print ballot, user_queues

  quantums = 0
  finished_processes = 0
  while True:
    misses = 0
    no_processes = False

    while True:
      owner = ballot.pop(0)
      user_queue = filter(lambda (a,b): a == owner, user_queues)[0]
      if user_queue:
        owner, owned_processes = user_queue
        available_processes = filter(lambda (a,b,c,d): c <= quantums,
        owned_processes)
      else:
        available_processes = []

      ballot.append(owner)
      if available_processes:
        name, owner, starttime, remaining = available_processes.pop(0)
        owned_processes = filter(lambda (a,b,c,d): a != name, owned_processes)
        user_queues = filter(lambda (a,b): a != owner, user_queues)
        break
      else:
        misses += 1
        if misses == len(ballot):
          no_processes = True
          break

    if no_processes:
      print "No processes running at time %i" % quantums
      quantums += 1
      if quantums >10:
        break
      continue
    else:
      if remaining >= 2:
        remaining -= 2
        increment = 2
      else:
        remaining = 0
        increment = 1

      print "From time %i to %i: %s remaining time: %i" % (quantums,
      quantums + increment, name, remaining)

      quantums += increment
      if remaining:
        owned_processes.append((name, owner, starttime, remaining))
      else:
        finished_processes += 1
        print "Process %s has finished" % name
        if finished_processes >= len(processes):
          break

      user_queues.append((owner, owned_processes))

print "Start of STR"
shortest_time_remaining([("A","Mohamed",1,3), ("B","Mohamed",2,1),
("C","Mohamed",3,1), ("D","Mohamed",8,3)])

print "\n\n"

print "Start of lottery"
processes = [("A","Mohamed",1,10), ("B","Nourhan",2,7), ("C","Mohamed",3,5), ("D","Nourhan",8,3)]
priorities = [("Mohamed", 5), ("Nourhan", 5)]
print processes
print priorities
lottery(processes, priorities)

print "\n\n"
print "Start of fair share"
fair_share(processes, priorities)
