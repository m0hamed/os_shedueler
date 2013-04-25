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
  # the lottery box
  box = []

  # for each process
  for (name, owner, starttime, remaining) in processes:
    # Get priority of the process
    username, priority = filter(lambda (a,b): a==owner, priorities)[0]
    # Add its tickets to the box
    box += [(name, starttime)]*priority

  # Start the clock
  quantums = 0
  while True:
    # Get the list of processes that can run at this time
    available = filter(lambda (a,b): b <= quantums, box)

    # If some processes can run
    if available:
      # Pick one at random from the box
      index = random.randrange(len(available))
      name, starttime = available[index]

      # get the process info
      name, user, starttime, remaining = \
        filter(lambda (a,b,c,d): a == name, processes)[0]

      # decrement the remaining time of the process
      remaining -= 2

      # remove it from the list of processes
      processes = filter(lambda (a,b,c,d): a != name, processes)

      if remaining > 0:
        # if it still has remaining time then add it back to the list
        processes.append((name, user, starttime, remaining))
        # The process has used its entire alocated time slot
        next_quantum = quantums + 2
      elif remaining == 0:
        # the process has used up its entire time slot and has finished
        next_quantum = quantums + 2
      else:
        # The process has finished but used up only half its alocated time
        remaining = 0
        # remove it from the  lottery box
        box = filter(lambda (a,b): a != name, box)
        next_quantum = quantums + 1

      print "From time %i to %i: %s remaining time: %i" % (quantums,
      next_quantum, name, remaining)

      # increment the clock
      quantums = next_quantum

      if remaining <= 0:
        print "Process %s has finished" % name
      if not processes:
        # All processes have finished
        break
    else:
      print "No processes are running at time %i" % quantums
      quantums += 1

def fair_share(processes=[], priorities=[]):
  # each user has a queue of processes
  user_queues = []
  # The shedule of the users
  scheduele = []

  for (owner, priority) in priorities:
    # the queue of processes belonging to the user
    queue = filter(lambda (a,b,c,d): b == owner, processes)
    # Add it to the list of queues
    user_queues.append((owner, queue))
    # add the user to the scheduele
    scheduele += [owner] * priority

  # shuffel the scheduele
  random.shuffle(scheduele)

  # start the clock
  quantums = 0
  finished_processes = 0
  while True:
    misses = 0
    no_processes = False

    while True:
      # get the next user from the schedule
      owner = scheduele.pop(0)
      # get his process queue
      user_queue = filter(lambda (a,b): a == owner, user_queues)[0]
      # if he has any processes
      if user_queue:
        owner, owned_processes = user_queue
        # get the processes that can run at this time
        available_processes = filter(lambda (a,b,c,d): c <= quantums,
        owned_processes)
      else:
        available_processes = []

      # return the user to the end of the scheduele
      scheduele.append(owner)

      if available_processes:
        # get the first runnable process from the user queue
        name, owner, starttime, remaining = available_processes.pop(0)
        # remove it from his queue
        owned_processes = filter(lambda (a,b,c,d): a != name, owned_processes)
        # remove his queue from the list of queues
        user_queues = filter(lambda (a,b): a != owner, user_queues)
        break
      else:
        # this user doesnt have any runnable processes
        # count the number of misses in th scheduele
        misses += 1
        # if looked over the entire scheduele and no user has runnable processes
        if misses == len(scheduele):
          no_processes = True
          break

    if no_processes:
      print "No processes running at time %i" % quantums
      quantums += 1
      continue
    else:
      # check if the currnt process will take its entire slot
      if remaining >= 2:
        # decrement its remaing time
        remaining -= 2
        # the clock will increment by 2
        increment = 2
      else:
        # the process is done and will use half its slot
        remaining = 0
        # the clock will increment by 1 slot
        increment = 1

      print "From time %i to %i: %s remaining time: %i" % (quantums,
      quantums + increment, name, remaining)

      quantums += increment

      if remaining:
        # the process is returned to the queue of the user
        owned_processes.append((name, owner, starttime, remaining))
      else:
        # count the number of finished processes
        finished_processes += 1
        print "Process %s has finished" % name

        # if all the processes finished then break
        if finished_processes >= len(processes):
          break

      if owned_processes:
        # return the amended user queue to the list of queues
        user_queues.append((owner, owned_processes))
      else:
        # remove the owner from the scheduele
        scheduele = filter(lambda a: a != owner, scheduele)

def process_print(process):
  print "Process %s, owner: %s, starting at clock %i and running for a total time of %i" % process

def user_print(user):
  print "User %s with priority: %i" % user

if __name__ == "__main__":
  print "Simulating Shortest time remaining"

  processes = [("A","Mohamed",1,3), ("B","Mohamed",2,1),
  ("C","Mohamed",3,1), ("D","Mohamed",8,3)]

  print "The list of processes are:"
  map(process_print, processes)

  shortest_time_remaining(processes)

  print "\n\n"

  print "Simultating lottery"

  processes = [("A","Mohamed",1,10), ("B","Nourhan",2,7), ("C","Mohamed",3,5), ("D","Nourhan",8,3)]
  priorities = [("Mohamed", 2), ("Nourhan", 7)]

  print "The list of processes are:"
  map(process_print, processes)
  print "The list of users are:"
  map(user_print, priorities)

  lottery(processes, priorities)

  print "\n\n"

  print "Simulating fair share"

  print "The list of processes are:"
  map(process_print, processes)
  print "The list of users are:"
  map(user_print, priorities)

  fair_share(processes, priorities)
